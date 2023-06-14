"""
The order


Lateral # done
Body Part #done
Reformat Plane
IV Contrast
Luminal Contrast (optional)
Dual Energy (optional)
Slice Thickness
Kernel
Reconstruction
Gating
Positioning
Section-Specific features
"""
import os
import pydicom as pd

body_part_dictionary = {
    "Chest": "Ch",
    "Whole Body": "WB",
    "Brain": "Brain",
    "Pituitary": "Pit",
    "Nasopharynx": "NP",
    "Oropharynx": "OP",
    "Temporal Mandibular Joint": "TMJ",
    "Abdomen": "Abd",
    "Prostate": "Pros",
    "Chest/Abdomen/Pelvis": "CAP",
    "Chest / Abdomen / Pelvis": "CAP",
    "Abdomen / Pelvis": "AbdPel",
    "Upper Extremity": "UExt",
    "Lower Extremity": "LExt",
    "Femur": "Fem",
    "Cervical": "Cer",
    "Thoracic": "TSp",
    "Lumbar": "LSp",
    "Sacroiliac Joint": "SIJ"
}


class ReadStudy:
    def __init__(self, study_dir):
        self.study_dir = study_dir
        list_files = os.listdir(self.study_dir)
        self.list_files_fn = [os.path.join(self.study_dir, _) for _ in list_files]

        self.ds = pd.read_file(self.list_files_fn[0], stop_before_pixels=True)
        self.body_part_examined = None

    def extract_laterality(self):
        pass

    def extract_body_part(self):
        try:
            self.body_part_examined = self.ds.BodyPartExamined
            print(self.body_part_examined)
        except:
            self.body_part_examined = None
            print("body part examined not found")
            return None
        else:

            if self.body_part_examined.title() in body_part_dictionary.keys():
                return body_part_dictionary[self.body_part_examined.title()]
            else:
                return self.body_part_examined

    def extractSeriesDescription(self):
        """
        Extract Series Description
        :return:
        """
        try:
            sd = self.ds.SeriesDescription
        except:
            sd = None
        return sd

    def look_for_projection(self):
        """
        Assuming that the projection information is available in SeriesDescription
        If the projection information is not available in SeriesDescription

        :return:
        """

        sd = self.extractSeriesDescription()
        if sd is None:
            proj = None
            print("Series Description is not available")
        else:
            if "MIP" in sd:
                proj = "MIP"
            elif "MinIP" in sd:
                proj = "MinIP"
            elif "MPR" in sd:
                proj = "MPR"
            elif "3D" in sd:
                proj = "3D"
            else:
                """
                At this point also look for this information in any other possible dicom field.
                """
                proj = "Primary"

            return proj

    def reformat_plane(self):
        """
        Extract reformat plane Axial coronal or sagittal
        There can be several ways of reading this information
        In this case we will extract from the ImageType

        :return:
        """
        try:
            imageType = self.ds.ImageType
            if "AXIAL" in imageType or "axial" in imageType or "Axial" in imageType:
                reformat_plane = "Ax"
            elif "CORONAL" in imageType or "coronal" in imageType or "Coronal" in imageType:
                reformat_plane = "Cor"
            elif "Sagittal" in imageType or "sagittal" in imageType or "Sagittal" in imageType:
                reformat_plane = "Sag"
            else:
                reformat_plane = None
        except:
            imageType = None
            reformat_plane = None

        return reformat_plane

    def IVContrast(self):
        """
        Extract IV Contrast from the tag [0x18, 0x10]
        :return: bool (True if Contrast False if no contrast)
        """
        con = None
        try:
            contrast = self.ds[0x018, 0x10]

        except:
            contrast = None
            print("Contrast info not found")
            con = self.IVContrast_from_image()

        else:
            if "Contrast" in contrast.name:
                con = "Con"

        return con

    def IVContrast_from_image(self):
        """
        Use Deep Learning tools to extract IV Contrast from images
        :return:
        """
        pass

    def dualenergy(self):
        pass

    def slice_thickness(self):
        """
        extract slice thickness
        :return:
        """
        try:
            st = self.ds.SliceThickness
        except:
            st = None
            print("Slice Thickness not available")

        if st is not None:
            if st < 1.0:
                return "Thinnest"
            elif st >= 1.0 and st < 2.5:
                return "Thin"
            elif st >= 2.5 and st < 5:
                return "Std"
            else:
                return "Thick"

    def modality(self):
        """
        Modality information
        :return:
        """
        try:
            modality = self.ds.Modality
        except:
            modality = None
            print("Modality not found")

        return modality

    def kernel(self):
        pass

    def reconstruction(self):
        pass

    def gating(self):
        pass

    def postioning(self):
        pass

    def other(self):
        pass
