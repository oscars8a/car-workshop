# -*- coding: utf-8 -*-
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html
from . import models, wizards
from odoo import api, _

def main(cr, registry):
    """
    En el nuevo tecnativa viene para poner el idioma inicial
    Esto sirve para cambiar el nombre del Proyecto "Repair and Revisiones".
    Si el idioma del admin es 'es_ES' cambia el nombre del proyecto a Reparaciones y revisiones.
    El nombre del proyecto es igual para todos los usuarios. En el caso de que la empresa tenga
    empleados con distintos idiomas se tendrá que decidir qué nombre poner.
    :param cr:
    :param registry:
    :return:
    """
    env = api.Environment(cr, 1, {})
    usuarios = env['res.users'].search([])
    espaniol = False
    for u in usuarios:
        if u.login == 'admin' and u.lang == 'es_ES':
            espaniol = True
    if espaniol:
        area_ids = env['project.project'].search([('car_work', '=', True)])
        if (len(area_ids) == 1):
            area = area_ids[0]
            area.write({'name': "Reparaciones y Revisiones"})