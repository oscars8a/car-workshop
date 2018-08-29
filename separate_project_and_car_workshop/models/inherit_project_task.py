# -*- coding: utf-8 -*-
from odoo import api, fields, models, _
from lxml import etree


class Task(models.Model):
    _inherit = 'project.task'

    @api.model
    def fields_view_get(self, view_id=None, view_type=None, toolbar=False, submenu=False):
        res = super(Task, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        doc = etree.XML(res['arch'])
        cw_projects = self.env['project.project'].search([('car_work', '=', True)]).ids
        if view_type == 'form':
        #     Nos aseguramos que la nueva tarea que se cree desde un Form no pertenezca a las areas de taller...
            nodes_field_project_id = doc.xpath("//field[@name='project_id']")
            for node in nodes_field_project_id:
                node.set(
                    'domain', str([
                        ('id', 'not in', cw_projects)
                    ])
                )
        res['arch'] = etree.tostring(doc)
        return res


    @api.model
    def search(self, args, offset=0, limit=None, order=None, count=False):
    # Metodo para quitar las tareas que son de Taller.
        cw_projects = self.env['project.project'].search([('car_work', '=', True)]).ids
        args.append(('project_id','not in',cw_projects))
        return super(Task, self).search(args, offset=offset, limit=limit, order=order, count=count)