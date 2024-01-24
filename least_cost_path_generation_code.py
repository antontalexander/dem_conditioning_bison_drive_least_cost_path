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

    cost_rasters_subfolder = os.path.join(rasters_folder, "cost_rasters").replace("\\", "/")

    dems_subfolder = os.path.join(rasters_folder, "dems").replace("\\", "/")

    slope_rasters_subfolder = os.path.join(rasters_folder, "slope_rasters").replace("\\", "/")

    buffers_subfolder = os.path.join(shapefiles_folder, "buffers").replace("\\", "/")

    cost_paths_subfolder = os.path.join(shapefiles_folder, "cost_paths").replace("\\", "/")

    lines_subfolder = os.path.join(shapefiles_folder, "lines").replace("\\", "/")

    points_subfolder = os.path.join(shapefiles_folder, "points").replace("\\", "/")

    end_point = os.path.join(points_subfolder, "end_point.shp").replace("\\", "/")

    selection = os.path.join(points_subfolder, "selection.shp").replace("\\", "/")

    merge = os.path.join(lines_subfolder, "merged_least_cost_paths.shp").replace("\\", "/")

    dem_name = "rh_dem_clp.tif"

    polyline_shapefile_list = []
    #
    # # generate buffers at 0.5km intervals
    # print "Generating buffers at 0.5km intervals"
    # for i in range(1, 11):
    #     buffer_distance = i * 0.5
    #     buffer_distance_with_units = str(buffer_distance) + " Kilometers"
    #     buffer_name = "{}_m_buffer.shp".format(str(i*500))
    #     buffer_output_file_path = os.path.join(buffers_subfolder, buffer_name).replace("\\", "/")
    #     arcpy.Buffer_analysis(end_point, buffer_output_file_path, buffer_distance_with_units)
    #     # turn buffers into polylines
    #     print "Turning buffer into polyline"
    #     line_name = "{}_m_buffer_line.shp".format(str(i*500))
    #     line_output_file_path = os.path.join(lines_subfolder, line_name).replace("\\", "/")
    #     arcpy.PolygonToLine_management(buffer_output_file_path, line_output_file_path)
    #     # turn polylines into points and delete duplicate points
    #     print "Turning polyline into points and deleting duplicate points"
    #     point_shapefile_name = "{}_m_buffer_line_points.shp".format(str(i*500))
    #     point_shapefile_output_file_path = os.path.join(points_subfolder,
    #                                                     point_shapefile_name).replace("\\", "/")
    #     arcpy.GeneratePointsAlongLines_management(line_output_file_path,
    #                                               point_shapefile_output_file_path,
    #                                               'PERCENTAGE', Percentage=5,
    #                                               Include_End_Points='END_POINTS')
    #     arcpy.DeleteIdentical_management(point_shapefile_output_file_path, "Shape")
    #     # delete buffer and polyline
    #     print "Deleting buffer and polyline"
    #     arcpy.Delete_management(buffer_output_file_path)
    #     arcpy.Delete_management(line_output_file_path)
    #     # perform field calculation on id to change it to 1
    #     field_name = "Id"
    #     expression = """1"""
    #     arcpy.CalculateField_management(point_shapefile_output_file_path, field_name, expression,
    #                                     "PYTHON_9.3")
    #     point_shapefile_list.append(point_shapefile_output_file_path)
    #
    # # generate slope raster with input dem
    # print 'Generating slope TIFF from DEM'
    # env.workspace = dems_subfolder
    arcpy.CheckOutExtension("Spatial")
    # slope_raster = Slope(dem_name, "DEGREE")
    # slope_output_file_path = os.path.join(slope_rasters_subfolder, "slope.tif").replace("\\", "/")
    # slope_raster.save(slope_output_file_path)
    #
    # # change values greater than or equal to zero and less than 1 to 1 to allow future tools to work
    # env.workspace = slope_rasters_subfolder
    conditional_slope_file_path = os.path.join(slope_rasters_subfolder, "con_slp.tif")
    # input_slope_raster = "slope.tif"
    # con_slp = Con(input_slope_raster, input_slope_raster, "1", "VALUE >= 1")
    # con_slp.save(conditional_slope_file_path)

    point_shapefile_list = [r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/500_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/1000_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/1500_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/2000_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/2500_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/3000_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/3500_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/4000_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/4500_m_buffer_line_points.shp',
                            r'C:/Users/aanton/Documents/archeology_lab_projects/south_dakota/2022/ree_heights_bison_kill/gis/shapefiles/points/5000_m_buffer_line_points.shp']

    # generate least cost path polylines for each point
    print "Begin Generating least cost paths for each point"
    distance_from_end_point = 500
    for point_shapefile in point_shapefile_list:
        distance_from_end_point_str = str(distance_from_end_point)
        fid = 0
        print "Distance from end point string built"
        for feature in point_shapefile:
            if fid == 20:
                break
            fid_string = str(fid)
            print "FID string built"
            cost_distance_file_path = os.path.join(cost_rasters_subfolder,
                                                    "cst_dst"
                                                    "{}_{}.tif".format(fid_string,
                                                                       distance_from_end_point_str
                                                                       )).replace("\\", "/")
            out_backlink_raster = os.path.join(cost_rasters_subfolder,
                                                    "bl"
                                                    "{}_{}.tif".format(fid_string,
                                                                       distance_from_end_point_str
                                                                       )).replace("\\", "/")
            fld_fid = "FID"
            where_clause = '"' + fld_fid + '" = ' + "" + fid_string + ""
            # select a specific point in the point shapefile
            print "Attempting to perform select analysis"
            arcpy.Select_analysis(point_shapefile, selection, where_clause)
            env.workspace = cost_rasters_subfolder
            arcpy.env.overwriteOutput = True
            # generate cost distance and backlink rasters for the point
            print "Generating cost distance and backlink rasters for " \
                  "point_{}_{}".format(fid_string, distance_from_end_point_str)
            out_cost_distance_raster = CostDistance(selection,
                                                    conditional_slope_file_path,
                                                    out_backlink_raster=out_backlink_raster)
            out_cost_distance_raster.save(cost_distance_file_path)
            # generate cost path as polyline
            print "generating cost path as a polyline"
            cost_path_file_path = os.path.join(cost_paths_subfolder,
                                               "cost_path_{}_{}.shp".format(fid_string,
                                                                            distance_from_end_point_str))
            CostPathAsPolyline(end_point, cost_distance_file_path,
                               out_backlink_raster, cost_path_file_path, path_type="BEST_SINGLE")

            print "Appending cost path file path to list"
            polyline_shapefile_list.append(cost_path_file_path)

            # delete rasters
            print "Deleting selection"
            arcpy.Delete_management(selection)
            arcpy.Delete_management(out_backlink_raster)
            arcpy.Delete_management(cost_distance_file_path)

            fid = fid + 1
        distance_from_end_point = distance_from_end_point + 500

    arcpy.management.Merge(polyline_shapefile_list, merge)

    print 'Program finished'

main()

