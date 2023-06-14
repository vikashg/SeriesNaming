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
    list_files = glob.glob(path + '/**/*.dcm', recursive=True)

    dir_list = []
    for _file in list_files:
        _dir = os.path.dirname(_file)
        dir_list.append(_dir)

    out_dir_list = list(set(dir_list))
    return out_dir_list



def main():
    pat_dir =
    out_dir_list = listdirs(pat_dir)
    print(len(out_dir_list))

    for _series_dir in out_dir_list:

        series_name = _series_dir.split('\\')[-1]
        rs = ReadStudy(_series_dir)
        body_part = rs.extract_body_part()
        reformat_pane = rs.reformat_plane()
        contrast = rs.IVContrast()
        proj = rs.look_for_projection()
        st = rs.slice_thickness()
        mod = rs.modality()
        seriesDes = rs.extractSeriesDescription()
        print("->", series_name)
        print(body_part, reformat_pane, proj, contrast, st, mod, seriesDes)
        print("+" * 20)

        cs = ConstructSeriesName()
        cs.body_part = body_part
        cs.acquisition_plane = reformat_pane
        cs.contrast = contrast
        cs.thickness = st
        cs.projection = proj
        print("CS ", cs.body_part, cs.acquisition_plane, cs.contrast, cs.thickness, cs.projection)


if __name__ == '__main__':
    main()