from typing import Any, Dict

import frappe
from frappe.model.document import Document

from vrtnext.abc.virtual_controller import VirtualController
from vrtnext.constants import Constants
from vrtnext.models.context.client_side_context import ClientSideContext
from vrtnext.models.document_metadata.redis_document_metadata import RedisDocumentMetadata
from vrtnext.typings.document_metadata import DocumentMetadata
from vrtnext.typings.pagination_options import PaginationOptions
from vrtnext.typings.virtual_dao import VirtualCountResponse, VirtuaListResponse
from vrtnext.utilities import Logger


class ClientSideController(VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    def db_insert(self, context: ClientSideContext, *args, **kwargs):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            creatable_doc = rest_mapper.map_doc_to_item(self.as_dict(), ignore_optional=True)

            redis_document_metadata = RedisDocumentMetadata()
            metadata = DocumentMetadata(
                owner="",
                modified_by="",
                modified="",
                creation="",
                docstatus=0,
                idx=0,
                _user_tags="",
                _liked_by="",
                _comments="",
                _assign="",
            )

            redis_document_metadata.set(self.doctype, self.as_dict().get(rest_mapper.name_column), metadata)

            dao.insert(data=creatable_doc)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw("Error saving the data.")

            Logger.Controller.error(e)

    def load_from_db(self, context: ClientSideContext):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            rest_response = dao.find_one_by_pk(self.name)

            redis_document_metadata = RedisDocumentMetadata()
            metadata = None
            if rest_response.data:
                metadata = redis_document_metadata.find_or_save(self.doctype, rest_response.data.get(rest_mapper.name_column))

            doc: Dict[str, Any] = {}

            rest_mapper.map_item_to_doc(rest_response.data, doc, metadata)

            print(f"DOC after: {doc}")

            # Using Document because frappe will make the site became 404 if not
            return super(Document, self).__init__(doc)

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw(f"Error loading data with name: {self.name}")

            Logger.Controller.error(e)

    def db_update(self, context: ClientSideContext):
        try:
            print(f"Self: {self}")
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            redis_document_metadata = RedisDocumentMetadata()
            redis_document_metadata.update_timestamp(self.doctype, self.name)

            updatable_doc = rest_mapper.map_doc_to_item(self, ignore_optional=True)

            dao.update(new_data=updatable_doc, name=self.name)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw(f"Error updating the data: {self.name}")

            Logger.Controller.error(e)

    @staticmethod
    def get_list(args, context: ClientSideContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            pagination_options = PaginationOptions(page_length=args.get("page_length", "20"), start=args.get("start", "0"))

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(options=pagination_options)

            mapped_filter = filterable.filters_mapper(filters=frappe_doc_filters)

            request_filters = None
            request_pagination = None

            is_client_side_pagination = mapped_pagination.get("is_client_side_paginator")
            is_client_side_filters = mapped_filter.get("is_client_side_filters")

            if not is_client_side_filters:
                request_filters = mapped_filter

            if not is_client_side_pagination:
                request_pagination = mapped_pagination

            response: VirtuaListResponse[Any, Any] = dao.find_all(
                filters=(request_filters or frappe_doc_filters),
                pagination=(request_pagination or {}),
            )

            data = []

            page_start = int(pagination_options.start)
            page_end = page_start + int(pagination_options.page_length) - 1

            for idx, item in enumerate(response.data):
                if is_client_side_pagination and not (page_start <= idx <= page_end):
                    continue

                redis_document_metadata = RedisDocumentMetadata()

                metadata = redis_document_metadata.find_or_save(args["doctype"], item[rest_mapper.name_column])

                doc: Dict[str, Any] = {}
                rest_mapper.map_item_to_doc(item, doc, metadata)

                data.append(doc)

            return data

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e)
            else:
                # We can't display application error in production.
                frappe.throw("Failed to show the document list.")

            Logger.Controller.error(e)

    @staticmethod
    def get_count(args, context: ClientSideContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()

            pagination_options = PaginationOptions(page_length=args.get("per_page", "20"), start=args.get("start", "0"))

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(options=pagination_options)

            mapped_filter = filterable.filters_mapper(filters=frappe_doc_filters)

            response: VirtualCountResponse[Any] = dao.get_item_count(
                filters=(mapped_filter or frappe_doc_filters),
                pagination=(mapped_pagination or {}),
            )

            return response.data

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(f"Failed to get the lists count: {e}")
            else:
                # Don't throw exception if the get_count is error.
                return 0

            Logger.Controller.error(e)

    @staticmethod
    def get_stats(args):
        pass
