import glob
import pydicom as pd
import os
from extractReader2 import ReadStudy
from ConstructSeriesName import ConstructSeriesName

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

def listdirs(path):
    """
    Extract the names of all subdirectories containing the dicom file
    :param path:
    :return:
    """
    list_files = glob.glob(path + '/**/*.dcm', recursive=True)

    dir_list = []
    for _file in list_files:
        _dir = os.path.dirname(_file)
        dir_list.append(_dir)

    out_dir_list = list(set(dir_list))
    return out_dir_list


def main():
    pat_dir = '/Users/m237134/Documents/SIIM/hackathon-images'
    out_dir_list = listdirs(pat_dir)

    for _series_dir in out_dir_list:
        series_name = _series_dir.split('\\')[-1]
        rs = ReadStudy(_series_dir)
        body_part = rs.extract_body_part() # Get the body part
        reformat_pane = rs.reformat_plane() # Get the acquisition plane
        contrast = rs.IVContrast() # Get Contrast information
        proj = rs.look_for_projection() # Get Projection either MIP or MinIP
        st = rs.slice_thickness() # Get Slice Thickness
        mod = rs.modality() # Get Modality
        seriesDes = rs.extractSeriesDescription()  # Extract Series Description



        # Reconstruct the new series name
        cs = ConstructSeriesName()
        cs.body_part = body_part
        cs.acquisition_plane = reformat_pane
        cs.contrast = contrast
        cs.thickness = st
        cs.projection = proj
        print("Name of the directory: ", _series_dir)
        print("Old Series Description: ", seriesDes)
        print("New Series Name: ", cs.body_part, cs.acquisition_plane, cs.contrast, cs.thickness, cs.projection)
        print("+"*20)


if __name__ == '__main__':
    main()