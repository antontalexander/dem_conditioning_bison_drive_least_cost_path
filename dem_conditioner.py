import os
import arcpy
import arcpy.management
from arcpy import env
from arcpy.sa import *

def main():

    base_folder = r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/' \
              r'ree_heights_bison_kill/gis'

    rasters_folder = os.path.join(base_folder, "rasters").replace("\\","/")

    shapefiles_folder = os.path.join(base_folder, "shapefiles").replace("\\","/")

    dems_subfolder = os.path.join(rasters_folder, "dems").replace("\\", "/")

    buffers_subfolder = os.path.join(shapefiles_folder, "buffers").replace("\\", "/")

    polygons_subfolder = os.path.join(shapefiles_folder, "polygons").replace("\\", "/")

    lines_subfolder = os.path.join(shapefiles_folder, "lines").replace("\\", "/")

    points_subfolder = os.path.join(shapefiles_folder, "points").replace("\\", "/")

    end_point = os.path.join(points_subfolder, "end_point.shp").replace("\\", "/")

    poly_selection = os.path.join(polygons_subfolder, "poly_selection.shp").replace("\\", "/")

    point_selection = os.path.join(points_subfolder, "point_selection.shp").replace("\\", "/")

    snap_raster = os.path.join(dems_subfolder, "rh_dem_clpCopy.tif").replace("\\", "/")

    route_pts = r"C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis" \
                r"/shapefiles/big_test/route_pts.shp"

    fishnet_with_points = r"C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill" \
                          r"/gis/shapefiles/big_test/fishnet_with_points.shp"

    ebk_raster_base_folder = r"C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022" \
                             r"/ree_heights_bison_kill/gis/rasters/ebk_rasters"

    dem_route_replacement = r"C:/Users/aanton/Documents/archeology_lab_projects/south_dakota" \
                            r"/2022/ree_heights_bison_kill/gis/shapefiles/dem_conditioning" \
                            r"/dem_route_replacement.shp"

    raster_mosaic_list = []

    output_location_number = 0

    fld_fid = "FID"
    fid = 0
    for feature in fishnet_with_points:
        #336
        if fid == 336:
            break
        fid_string = str(fid)
        print "FID string built"

        where_clause = '"' + fld_fid + '" = ' + "" + fid_string + ""
        # select a specific point in the point shapefile
        print "Attempting to select polygon with FID {}".format(fid_string)
        arcpy.Select_analysis(fishnet_with_points, poly_selection, where_clause)
        print "Polygon selected"

        fishnet_layer = "fishnet_lyr"
        arcpy.MakeFeatureLayer_management(fishnet_with_points, fishnet_layer)
        print "Selecting fishnet polygons intersecting polygon with FID {}".format(fid_string)
        arcpy.SelectLayerByLocation_management(fishnet_layer, overlap_type="INTERSECT"
                                               , select_features=poly_selection)
        print "Fishnet polygons intersecting primary fishnet polygon selected"

        route_pts_layer = "route_pts_lyr"
        arcpy.MakeFeatureLayer_management(route_pts, route_pts_layer)
        print "Selecting route points using the previously created fishnet polygons shapefile"
        arcpy.SelectLayerByLocation_management(route_pts_layer, overlap_type="INTERSECT",
                                               select_features="fishnet_lyr")

        arcpy.CopyFeatures_management(route_pts_layer, point_selection)

        print "Clearing previous selections"
        arcpy.SelectLayerByAttribute_management(fishnet_layer, selection_type="CLEAR_SELECTION")
        arcpy.SelectLayerByAttribute_management(route_pts_layer, selection_type="CLEAR_SELECTION")

        print "Setting up EBK"
        ebk_raster = os.path.join(ebk_raster_base_folder, "ebk{}.tif".format(fid_string)).replace("\\", "/")

        # Set environment settings
        arcpy.env.workspace = ebk_raster_base_folder
        arcpy.env.snapRaster = snap_raster

        # Set local variables
        inPointFeatures = point_selection
        zField = "grid_code"
        outRaster = ebk_raster
        cellSize = 1
        maxLocalPoints = 500
        overlapFactor = 5
        numberSemivariograms = 100
        # Set variables for search neighborhood
        radius = 200
        angle = 0
        nbrMax = 500
        nbrMin = 100
        sectorType= "EIGHT_SECTORS"
        searchNeighbourhood = arcpy.SearchNeighborhoodStandardCircular(radius, angle, nbrMax, nbrMin,
                                                                       sectorType)
        outputType = "PREDICTION"
        quantileValue = ""
        thresholdType = ""
        probabilityThreshold = ""
        semivariogram = "POWER"
        # Check out the ArcGIS Geostatistical Analyst extension license
        arcpy.CheckOutExtension("GeoStats")

        # Execute EmpiricalBayesianKriging
        print "Executing EBK"
        arcpy.EmpiricalBayesianKriging_ga(inPointFeatures, zField, out_raster=outRaster,
                                          cell_size=cellSize, max_local_points=maxLocalPoints,
                                          overlap_factor=overlapFactor,
                                          number_semivariograms=numberSemivariograms,
                                          search_neighborhood=searchNeighbourhood, output_type=outputType,
                                          semivariogram_model_type = semivariogram)

        print "Extracting EBK raster with routes polygons"
        clipped_ebk_file_path = os.path.join(ebk_raster_base_folder, "ebk_clip_{}.tif".format(fid_string))
        clipped_ebk_raster = clipped_ebk_file_path.replace("\\", "/")
        arcpy.CheckOutExtension("Spatial")
        inRaster = ebk_raster
        outExtractByMask = ExtractByMask(inRaster, dem_route_replacement)
        outExtractByMask.save(clipped_ebk_raster)

        print "Extracting extracted EBK raster to selected fishnet"
        fishnet_ebk_raster = os.path.join(ebk_raster_base_folder, "ebk_fn_{}.tif".
                                          format(fid_string)).replace("\\", "/")
        inRaster = clipped_ebk_raster
        outExtractByMask = ExtractByMask(inRaster, poly_selection)
        outExtractByMask.save(fishnet_ebk_raster)

        print "Deleting selections and intermediate rasters"
        arcpy.Delete_management(poly_selection)
        arcpy.Delete_management(point_selection)
        arcpy.Delete_management(ebk_raster)
        arcpy.Delete_management(clipped_ebk_raster)
        arcpy.Delete_management(fishnet_layer)
        arcpy.Delete_management(route_pts_layer)

        raster_mosaic_list.append(fishnet_ebk_raster)
        fid += 1

    for raster in raster_mosaic_list:
        #336
        if output_location_number == 336:
            break
        output_location_number_string = str(output_location_number)
        print "Creating raster mosaic {}".format(output_location_number_string)
        env.workspace = dems_subfolder
        if output_location_number == 0:
            mosaicked_raster = "mos_ras_{}.tif".format(output_location_number_string)
            arcpy.MosaicToNewRaster_management([raster, snap_raster], output_location=dems_subfolder,
                                               raster_dataset_name_with_extension=mosaicked_raster,
                                               pixel_type="32_BIT_FLOAT", cellsize=1, number_of_bands=1,
                                               mosaic_method="FIRST", mosaic_colormap_mode="LAST")
        else:
            previous_raster_mosaic_number = output_location_number - 1
            previous_raster_mosaic_number_string = str(previous_raster_mosaic_number)
            previous_raster_mosaic = "mos_ras_{}.tif".format(previous_raster_mosaic_number_string)
            mosaicked_raster = "mos_ras_{}.tif".format(output_location_number_string)
            arcpy.MosaicToNewRaster_management([raster, previous_raster_mosaic],
                                               output_location=dems_subfolder,
                                               raster_dataset_name_with_extension=mosaicked_raster,
                                               pixel_type="32_BIT_FLOAT", cellsize=1, number_of_bands=1,
                                               mosaic_method="FIRST", mosaic_colormap_mode="LAST")
            print "Deleting previous raster mosaic"
            arcpy.Delete_management(previous_raster_mosaic)
        output_location_number += 1

main()
