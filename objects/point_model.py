# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Qgis2threejs
                                 A QGIS plugin
 export terrain data, map canvas image and vector data to web browser
                             -------------------
        begin                : 2014-01-19
        copyright            : (C) 2014 Minoru Akagi
        email                : akaginch@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.core import QGis
from Qgis2threejs.stylewidget import StyleWidget

def geometryType():
  return QGis.Point

def objectTypeNames():
  return ["JSON model", "COLLADA model"]

def setupWidgets(ppage, mapTo3d, layer, type_index=0):

  if type_index == 0:
    name = "JSON file"
    filterString = "JSON files (*.json *.js);;All files (*.*)"
    rotationX = 90
  else:
    name = "COLLADA file"
    filterString = "COLLADA files (*.dae);;All files (*.*)"
    rotationX = 0

  ppage.initStyleWidgets(color=False, transparency=False)
  ppage.addStyleWidget(StyleWidget.FILEPATH, {"name": name, "layer": layer, "filterString": filterString})
  ppage.addStyleWidget(StyleWidget.FIELD_VALUE, {"name": "Scale", "defaultValue": 1, "layer": layer})
  ppage.addStyleWidget(StyleWidget.FIELD_VALUE, {"name": "Rotation (x)", "label": "Degrees", "defaultValue": rotationX, "layer": layer})
  ppage.addStyleWidget(StyleWidget.FIELD_VALUE, {"name": "Rotation (z)", "label": "Degrees", "defaultValue": 0, "layer": layer})

def write(writer, layer, feat):
  vals = feat.propValues()
  model_path = vals[0]

  if feat.prop.type_index == 0:
    model_type = "JSON"
  else:
    model_type = "COLLADA"

  index = writer.modelManager.modelIndex(model_path, model_type)
  scale = float(vals[1])
  rotationX = float(vals[2])
  rotationZ = float(vals[3])
  writer.writeFeature({"model_index": index, "pts": feat.geom.asList(), "rotateX": rotationX, "rotateY": rotationZ, "scale": scale})
