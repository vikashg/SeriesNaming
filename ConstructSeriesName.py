import os


# V4 Series name structure : body_part
#                            reformat_plane/acquisition_plane
#                            Contrast/NonContrast
#                            Thickness Information
#                            projection

class ConstructSeriesName:
    def __init__(self):
        self._body_part = None
        self._acquisition_plane = None
        self._contrast = None
        self._thickness = None
        self._projection = None

    @property
    def body_part(self):
        return self._body_part

    @body_part.setter
    def body_part(self, value):
        self._body_part = value


    @property
    def acquisition_plane(self):
        return self._acquisition_plane

    @acquisition_plane.setter
    def acquisition_plane(self, value):
        self._acquisition_plane = value

    @property
    def contrast(self):
        return self._contrast

    @contrast.setter
    def contrast(self, value):
        self._contrast = value

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        self._thickness = value

    @property
    def projection(self):
        return self._projection

    @projection.setter
    def projection(self, value):
        self._projection = value

