from typing import Optional

import frappe

from dulnext.controllers.virtual_controller import VirtualController
from dulnext.exceptions import DependencyNotInjectedException
from dulnext.mapper.rest_mapper import RestMapper
from dulnext.utilities import LOGGER


class RestController(VirtualController):
    """Class For controlling Rest API Virtual Doctypes"""

    _rest_mapper: Optional[RestMapper] = None

    def __init__(self, rest_mapper: RestMapper, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._rest_mapper = rest_mapper

    def get_rest_mapper(self) -> RestMapper:
        if not self._rest_mapper:
            raise DependencyNotInjectedException("Failed to get the RestMapper")

        return self._rest_mapper

    def db_insert(self, *args, **kwargs):
        try:
            rest_mapper = self.get_rest_mapper()
            creatable_doc = rest_mapper.map_doc_to_rest(self, ignore_optional=True)

            model = self.get_virtual_dao()
            model.save(**creatable_doc)
        except Exception as e:
            if frappe.conf.get("development_mode") == 1:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw("Something went wrong")
            LOGGER.error(e)

    def load_from_db(self):
        try:
            model = self.get_virtual_dao()
            rest_repsonse = model.find_one_by_pk(self.name)

            rest_mapper = self.get_rest_mapper()

            doc = rest_mapper.map_rest_to_doc(rest_repsonse, self)

            return super().__init__(doc)

        except Exception as e:
            if frappe.conf.get("development_mode") == 1:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw("Something went wrong")
            LOGGER.error(e)

    def db_update(self):
        try:
            rest_mapper = self.get_rest_mapper()
            updatable_doc = rest_mapper.map_doc_to_rest(self, ignore_optional=True)

            model = self.get_virtual_dao()
            model.update(**updatable_doc)
        except Exception as e:
            if frappe.conf.get("development_mode") == 1:
                frappe.throw(e.message)
            else:
                # We can't display application error in production.
                frappe.throw("Something went wrong")
            LOGGER.error(e)

    # @staticmethod
    # def get_list(args):
    #     try:
    #          mapped_filter = cls.filters_mapper(args["filters"])

    #          model = self.get_virtual_dao()
    #          rest_repsonse = model.find_one_by_pk(self.name)

    #          rest_mapper = self.get_rest_mapper()

    #          doc = rest_mapper.map_rest_to_doc(rest_repsonse, self)

    #          return super(RestController, self).__init__(doc)

    #     except Exception as e:
    #         if frappe.conf.get("development_mode") == 1:
    #             frappe.throw(e.message)
    #         else:
    #             # We can't display application error in production.
    #             frappe.throw("Something went wrong")
    #         LOGGER.error(e)

    #     try:

    #         pagination = parse_pagination(args)
    #         print(args)
    #         users = SYNAPSEFI_CLIENT.get_all_users(
    #             per_page=pagination.per_page, page=pagination.page
    #         )

    #         SynapticUser.users_count = users.users_count

    #         user_lists = []

    #         for user in users.list_of_users:
    #             user_temp = SynapseUserMapper.map_user(user.body)

    #             user_lists.append(user_temp)

    #         return user_lists
    #     except SynapseError as se:
    #         frappe.throw(se.message)

    # @staticmethod
    # def get_count(args):
    #     return SynapticUser.users_count

    # @staticmethod
    # def get_stats(args):
    #     pass
