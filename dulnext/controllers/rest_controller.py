from typing import Any

import frappe
from frappe.model.document import Document

from dulnext.constants import Constants
from dulnext.controllers.virtual_controller import VirtualController
from dulnext.models.rest_context import RestContext
from dulnext.typings.pagination_options import PaginationOptions
from dulnext.typings.virtual_dao import VirtualCountResponse, VirtuaListResponse
from dulnext.utilities import LOGGER


# We Should make VirtualServices that are contains all rest_mapper, virtual_dao, filterable, and paginated to make it more modular
class RestController(VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    def __init__(
        self,
        rest_context: RestContext,
        *args,
        **kwargs,
    ):
        super().__init__(
            rest_context,
            *args,
            **kwargs,
        )

    def db_insert(self, *args, **kwargs):
        try:
            context = self.get_virtual_context()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()
            creatable_doc = rest_mapper.map_doc_to_item(self, ignore_optional=True)

            dao.insert(data=creatable_doc)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw("Error saving the data.")

            LOGGER.error(e)

    def load_from_db(self):
        try:
            context = self.get_virtual_context()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            rest_response = dao.find_one_by_pk(self.name)

            doc = rest_mapper.map_item_to_doc(rest_response, self)

            # Using Document because frappe will make the site became 404 if not
            return super(Document, self).__init__(doc)

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw(f"Error loading data with name: {self.name}")

            LOGGER.error(e)

    def db_update(self):
        try:
            context = self.get_virtual_context()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            updatable_doc = rest_mapper.map_doc_to_item(self, ignore_optional=True)

            dao.update(new_data=updatable_doc, name=self.name)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw(f"Error updating the data: {self.name}")

            LOGGER.error(e)

    @staticmethod
    def get_list(args, context: RestContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()
            rest_mapper = context.get_mapper()

            pagination_options = PaginationOptions(page_length=args.get("per_page", 20), start=args.get("start", 0))

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(options=pagination_options)

            mapped_filter = filterable.filters_mapper(filters=frappe_doc_filters)

            response: VirtuaListResponse[Any, Any] = dao.find_all(
                filters=(mapped_filter or frappe_doc_filters),
                pagination=(mapped_pagination or {}),
            )

            data = []

            for item in response.data:
                doc = rest_mapper.map_item_to_doc(item, RestController.doctype)
                data.append(doc)

            return data

        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e)
            else:
                # We can't display application error in production.
                frappe.throw(f"Failed to show the {RestController.doctype} list.")

            LOGGER.error(e)

    @staticmethod
    def get_count(args, context: RestContext):
        try:
            paginated = context.get_pagination_mapper()
            filterable = context.get_filter_mapper()
            dao = context.get_dao()

            pagination_options = PaginationOptions(page_length=args.get("per_page", 20), start=args.get("start", 0))

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
