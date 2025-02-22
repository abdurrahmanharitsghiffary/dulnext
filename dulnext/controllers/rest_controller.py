from typing import Any

import frappe
from frappe.model.document import Document

from dulnext.constants import Constants
from dulnext.controllers.virtual_controller import VirtualController
from dulnext.models.context.rest_context import VirtualContext
from dulnext.typings.pagination_options import PaginationOptions
from dulnext.typings.virtual_dao import VirtualCountResponse, VirtuaListResponse
from dulnext.utilities import LOGGER


class RestController(VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    def db_insert(self, context: VirtualContext, *args, **kwargs):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            creatable_doc = rest_mapper.map_doc_to_item(self.as_dict(), ignore_optional=True)

            dao.insert(data=creatable_doc)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw("Error saving the data.")

            LOGGER.error(e)

    def load_from_db(self, context: VirtualContext):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            rest_response = dao.find_one_by_pk(self.name)

            doc = rest_mapper.map_item_to_doc(rest_response.data, {})

            print(f"DOC after: {doc}")

            # Using Document because frappe will make the site became 404 if not
            return super(Document, self).__init__(doc)

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw(f"Error loading data with name: {self.name}")

            LOGGER.error(e)

    def db_update(self, context: VirtualContext):
        try:
            context = self.get_virtual_context()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            updatable_doc = rest_mapper.map_doc_to_item(self, ignore_optional=True)

            dao.update(new_data=updatable_doc, name=self.name)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw(f"Error updating the data: {self.name}")

            LOGGER.error(e)

    @staticmethod
    def get_list(args, context: VirtualContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()
            print(f"ARGS: {args}")
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

            print(f"Page Start: {page_start}")
            print(f"Page End: {page_end}")

            for idx, item in enumerate(response.data):
                if is_client_side_pagination and not (page_start <= idx <= page_end):
                    continue

                data.append(rest_mapper.map_item_to_doc(item, {}))

            return data

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e)
            else:
                # We can't display application error in production.
                frappe.throw("Failed to show the document list.")

            LOGGER.error(e)

    @staticmethod
    def get_count(args, context: VirtualContext):
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

            LOGGER.error(e)

    @staticmethod
    def get_stats(args):
        pass
