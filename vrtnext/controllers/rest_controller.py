from typing import Any, Dict

import frappe
from frappe.model.document import Document

from vrtnext.abc.virtual_controller import VirtualController
from vrtnext.constants import Constants
from vrtnext.models.context.rest_context import RestContext
from vrtnext.typings.pagination_options import PaginationOptions
from vrtnext.typings.virtual_dao import VirtualCountResponse, VirtuaListResponse
from vrtnext.utilities import Logger


class RestController(VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    def db_insert(self, context: RestContext, *args, **kwargs):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            creatable_doc = rest_mapper.map_doc_to_item(
                self.as_dict(), ignore_optional=True
            )

            dao.insert(data=creatable_doc)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw("Error saving the data.")

            Logger.Controller.error(e)

    def load_from_db(self, context: RestContext):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            rest_response = dao.find_one_by_pk(self.name)
            doc: Dict[str, Any] = {}
            rest_mapper.map_item_to_doc(rest_response.data, doc)

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

    def db_update(self, context: RestContext):
        try:
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            updatable_doc = rest_mapper.map_doc_to_item(
                self, ignore_optional=True
            )

            dao.update(new_data=updatable_doc, name=self.name)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(str(e))
            else:
                # We can't display application error in production.
                frappe.throw(f"Error updating the data: {self.name}")

            Logger.Controller.error(e)

    @staticmethod
    def get_list(args, context: RestContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            pagination_options = PaginationOptions(
                page_length=args.get("page_length", "20"),
                start=args.get("start", "0"),
            )

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(
                options=pagination_options
            )

            mapped_filter = filterable.filters_mapper(
                filters=frappe_doc_filters
            )

            response: VirtuaListResponse[Any, Any] = dao.find_all(
                filters=(mapped_filter or frappe_doc_filters),
                pagination=(mapped_pagination or {}),
            )

            data = []

            for item in response.data:
                doc: Dict[str, Any] = {}
                rest_mapper.map_item_to_doc(item, doc)
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
    def get_count(args, context: RestContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()

            pagination_options = PaginationOptions(
                page_length=args.get("per_page", "20"),
                start=args.get("start", "0"),
            )

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(
                options=pagination_options
            )

            mapped_filter = filterable.filters_mapper(
                filters=frappe_doc_filters
            )

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
