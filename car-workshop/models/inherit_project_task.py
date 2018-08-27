# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from lxml import etree
from wdb import set_trace as depurador


class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def fields_view_get(self, view_id=None, view_type=None, toolbar=False, submenu=False):

        # depurador()
        res = super(Task, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        cw_projects = self.env['project.project'].search([('car_work', '=', True)]).ids
        print(view_type)
        if view_type == 'form':
        #     Nos aseguramos que la nueva tarea que se cree desde un Form no pertenezca a las areas de taller...
            nodes_field_project_id = doc.xpath("//field[@name='project_id']")
            for node in nodes_field_project_id:
                node.set(
                    'domain', str([
                        ('id', 'not in', cw_projects)
                    ])
                )
        if view_type == 'search':
            attrib = {
                'name':'single_tasks'
            }
            single_tasks = etree.Element('filter',attrib)
            tree = doc.find("tree")
            print(etree.tostring(doc))
        res['arch'] = etree.tostring(doc)
        return res

    # @api.model
    # def fields_view_get(self, view_id=None, view_type=False,
    #                     context=None, toolbar=False, submenu=False):
    #     """ Sobreescritura de la función fields_view_get del modelo
    #     res.partner para permitir usar dominios complejos en dos filtros
    #     nuevos definidos en la vista con id externo
    #     solivera_res_partner_filter_inherited_view_search.
    #     Se trata de filtrar usuarios en el menú Clientes de Odoo:
    #     1) Clientes que sólo son responsables
    #     2) Clientes que sólo son comensales
    #     :param view_id:
    #     :param view_type:
    #     :param context:
    #     :param toolbar:
    #     :param submenu:
    #     :return:
    #     """
    #     res = super(ResPartner, self).fields_view_get(
    #         view_id=view_id, view_type=view_type, context=context,
    #         toolbar=toolbar, submenu=submenu)
    #     doc = etree.XML(res['arch'])
    #     if view_type == 'search':
    #         # 1. Filtrar partners que sólo son responsables
    #         node_filter_responsible = \
    #             doc.xpath("//filter[@name='responsible']")
    #         responsibles = \
    #             self.env['solivera.responsible'].search([]).mapped(
    #                 'partner').ids
    #         for node in node_filter_responsible:
    #             node.set('domain', "[('id', 'in'," + str(responsibles) + ")]")
    #
    #         # 2. Filtrar partners que sólo son comensales
    #         node_filter_children = \
    #             doc.xpath("//filter[@name='children']")
    #         children = \
    #             self.env['solivera.children'].search([]).mapped('partner').ids
    #         for node in node_filter_children:
    #             node.set('domain', "[('id', 'in'," + str(children) + ")]")
    #         res['arch'] = etree.tostring(doc)
    #     return res