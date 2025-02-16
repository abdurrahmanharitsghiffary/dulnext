from typing import Any, Optional

import frappe
from frappe.model.document import Document

from dulnext.constants import Constants
from dulnext.controllers.virtual_controller import VirtualController
from dulnext.exceptions import MissingDependencyError
from dulnext.mapper.rest_mapper import RestMapper
from dulnext.models.filterable import Filterable
from dulnext.models.paginated import Paginated
from dulnext.models.virtual_dao import VirtualDAO
from dulnext.typings.pagination_options import PaginationOptions
from dulnext.typings.virtual_dao import VirtualCountResponse, VirtuaListResponse
from dulnext.utilities import LOGGER


class RestController(VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    _rest_mapper: Optional[RestMapper] = None

    def __init__(
        self,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
        filterable: Filterable,
        paginated: Paginated,
        *args,
        **kwargs,
    ):
        super().__init__(
            virtual_dao,
            paginated,
            filterable,
            *args,
            **kwargs,
        )
        self._rest_mapper = rest_mapper

    def get_rest_mapper(self) -> RestMapper:
        if not self._rest_mapper:
            raise MissingDependencyError("Failed to get the RestMapper")

        return self._rest_mapper

    def db_insert(self, *args, **kwargs):
        try:
            rest_mapper = self.get_rest_mapper()
            creatable_doc = rest_mapper.map_doc_to_rest(self, ignore_optional=True)

            model = self.get_virtual_dao()
            model.insert(data=creatable_doc)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw("Error saving the data.")

            LOGGER.error(e)

    def load_from_db(self):
        try:
            model = self.get_virtual_dao()
            rest_response = model.find_one_by_pk(self.name)

            rest_mapper = self.get_rest_mapper()

            doc = rest_mapper.map_rest_to_doc(rest_response, self.doctype)

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
            rest_mapper = self.get_rest_mapper()
            updatable_doc = rest_mapper.map_doc_to_rest(self, ignore_optional=True)

            model = self.get_virtual_dao()
            model.update(new_data=updatable_doc, name=self.name)
        except Exception as e:
            if Constants.IS_DEVELOPMENT_MODE:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw(f"Error updating the data: {self.name}")

            LOGGER.error(e)

    @staticmethod
    def get_list(
        args,
        filterable: Filterable,
        paginated: Paginated,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
    ):
        try:
            pagination_options = PaginationOptions(page_length=args.get("per_page", 20), start=args.get("start", 0))

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(pagination=pagination_options)

            mapped_filter = filterable.filters_mapper(filters=frappe_doc_filters)

            response: VirtuaListResponse[Any, Any] = virtual_dao.find_all(
                filters=(mapped_filter or frappe_doc_filters),
                pagination=(mapped_pagination or pagination_options),
            )

            data = []

            for item in response.data:
                doc = rest_mapper.map_rest_to_doc(item, RestController.doctype)
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
    def get_count(
        args,
        filterable: Filterable,
        paginated: Paginated,
        rest_mapper: RestMapper,
        virtual_dao: VirtualDAO,
    ):
        try:
            pagination_options = PaginationOptions(page_length=args.get("per_page", 20), start=args.get("start", 0))

            frappe_doc_filters = args.get("filters", {})

            mapped_pagination = paginated.pagination_mapper(pagination=pagination_options)

            mapped_filter = filterable.filters_mapper(filters=frappe_doc_filters)

            response: VirtualCountResponse[Any] = virtual_dao.get_item_count(
                filters=(mapped_filter or frappe_doc_filters),
                pagination=(mapped_pagination or pagination_options),
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
