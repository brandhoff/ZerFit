# -*- coding: utf-8 -*-

from pyueye import ueye
import numpy as np

class IdsCamera:
    _is_SetExposureTime = ueye._bind("is_SetExposureTime",
                                     [ueye.ctypes.c_uint, ueye.ctypes.c_double,
                                      ueye.ctypes.POINTER(ueye.ctypes.c_double)], ueye.ctypes.c_int)
    IS_GET_EXPOSURE_TIME = 0x8000

    @staticmethod
    def is_SetExposureTime(hCam, EXP, newEXP):
        """
        Description

        The function is_SetExposureTime() sets the with EXP indicated exposure time in ms. Since this
        is adjustable only in multiples of the time, a line needs, the actually used time can deviate from
        the desired value.

        The actual duration adjusted after the call of this function is readout with the parameter newEXP.
        By changing the window size or the readout timing (pixel clock) the exposure time set before is changed also.
        Therefore is_SetExposureTime() must be called again thereafter.

        Exposure-time interacting functions:
            - is_SetImageSize()
            - is_SetPixelClock()
            - is_SetFrameRate() (only if the new image time will be shorter than the exposure time)

        Which minimum and maximum values are possible and the dependence of the individual
        sensors is explained in detail in the description to the uEye timing.

        Depending on the time of the change of the exposure time this affects only with the recording of
        the next image.

        :param hCam: c_uint (aka c-type: HIDS)
        :param EXP: c_double (aka c-type: DOUBLE) - New desired exposure-time.
        :param newEXP: c_double (aka c-type: double *) - Actual exposure time.
        :returns: IS_SUCCESS, IS_NO_SUCCESS

        Notes for EXP values:

        - IS_GET_EXPOSURE_TIME Returns the actual exposure-time through parameter newEXP.
        - If EXP = 0.0 is passed, an exposure time of (1/frame rate) is used.
        - IS_GET_DEFAULT_EXPOSURE Returns the default exposure time newEXP Actual exposure time
        - IS_SET_ENABLE_AUTO_SHUTTER : activates the AutoExposure functionality.
          Setting a value will deactivate the functionality.
          (see also 4.86 is_SetAutoParameter).
        """
        _hCam = ueye._value_cast(hCam, ueye.ctypes.c_uint)
        _EXP = ueye._value_cast(EXP, ueye.ctypes.c_double)
        ret = IdsCamera._is_SetExposureTime(_hCam, _EXP, ueye.ctypes.byref(newEXP) if newEXP is not None else None)
        return ret

    def __init__(self, selector=''):
        self.hCam = ueye.HIDS(0)  # 0: first available camera;  1-254: The camera with the specified camera ID
        self.sInfo = ueye.SENSORINFO()
        self.cInfo = ueye.CAMINFO()
        self.pcImageMemory = ueye.c_mem_p()
        self.MemID = ueye.INT()
        self.rectAOI = ueye.IS_RECT()
        self.pitch = ueye.INT()
        self.nBitsPerPixel = ueye.INT()
        self.m_nColorMode = ueye.INT()
        self.bytes_per_pixel = 0
        self.width = ueye.INT()
        self.height = ueye.INT()
        self.size = (-1, -1)
        self.ok = False
        self.error_str = ''
        self.last_frame = None

    def _error(self, err_str):
        self.error_str = err_str
        return

    def connect(self):
        self.error_str = ''

        # Starts the driver and establishes the connection to the camera
        rc = ueye.is_InitCamera(self.hCam, None)
        print(rc)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_InitCamera ERROR")

        # Reads out the data hard-coded in the non-volatile camera memory
        # and writes it to the data structure that cInfo points to
        rc = ueye.is_GetCameraInfo(self.hCam, self.cInfo)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_GetCameraInfo ERROR")

        # You can query additional information about the sensor type used in the camera
        rc = ueye.is_GetSensorInfo(self.hCam, self.sInfo)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_GetSensorInfo ERROR")

        rc = ueye.is_ResetToDefault(self.hCam)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_ResetToDefault ERROR")

        # Set display mode to DIB
        rc = ueye.is_SetDisplayMode(self.hCam, ueye.IS_SET_DM_DIB)

        # Set the right color mode
        if int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_BAYER:
            # setup the color depth to the current windows setting
            ueye.is_GetColorDepth(self.hCam, self.nBitsPerPixel, self.m_nColorMode)
            self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
            print("IS_COLORMODE_BAYER: ", )

        elif int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_CBYCRY:
            # for color camera models use RGB32 mode
            self.m_nColorMode = ueye.IS_CM_BGRA8_PACKED
            self.nBitsPerPixel = ueye.INT(32)
            self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
            print("IS_COLORMODE_CBYCRY: ", )

        elif int.from_bytes(self.sInfo.nColorMode.value, byteorder='big') == ueye.IS_COLORMODE_MONOCHROME:
            # for color camera models use RGB32 mode
            self.m_nColorMode = ueye.IS_CM_MONO8
            self.nBitsPerPixel = ueye.INT(8)
            self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
            print("IS_COLORMODE_MONOCHROME: ", )

        else:
            # for monochrome camera models use Y8 mode
            self.m_nColorMode = ueye.IS_CM_MONO8
            self.nBitsPerPixel = ueye.INT(8)
            self.bytes_per_pixel = int(self.nBitsPerPixel / 8)
            print("Color mode: not identified")

        print("\tm_nColorMode: \t\t", self.m_nColorMode)
        print("\tnBitsPerPixel: \t\t", self.nBitsPerPixel)
        print("\tbytes_per_pixel: \t\t", self.bytes_per_pixel)
        print()

        # Can be used to set the size and position of an "area of interest"(AOI) within an image
        rc = ueye.is_AOI(self.hCam, ueye.IS_AOI_IMAGE_GET_AOI, self.rectAOI, ueye.sizeof(self.rectAOI))
        if rc != ueye.IS_SUCCESS:
            return self._error("is_AOI ERROR")

        self.width = self.rectAOI.s32Width
        self.height = self.rectAOI.s32Height
        self.size = (self.width.value, self.height.value)

        # Prints out some information about the camera and the sensor
        print("Camera model:\t\t", self.sInfo.strSensorName.decode('utf-8'))
        print("Camera serial no.:\t", self.cInfo.SerNo.decode('utf-8'))
        print("Camera image size:\t", str(self.size))
        print()

        # Allocates an image memory for an image having its dimensions defined by width and height
        # and its color depth defined by nBitsPerPixel
        rc = ueye.is_AllocImageMem(self.hCam, self.width, self.height,
                                   self.nBitsPerPixel, self.pcImageMemory, self.MemID)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_AllocImageMem ERROR")
        else:
            # Makes the specified image memory the active memory
            rc = ueye.is_SetImageMem(self.hCam, self.pcImageMemory, self.MemID)
            if rc != ueye.IS_SUCCESS:
                return self._error("is_SetImageMem ERROR")
            else:
                # Set the desired color mode
                rc = ueye.is_SetColorMode(self.hCam, self.m_nColorMode)

        # Activates the camera's live video mode (free run mode)
        rc = ueye.is_CaptureVideo(self.hCam, ueye.IS_DONT_WAIT)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_CaptureVideo ERROR")

        # Enables the queue mode for existing image memory sequences
        rc = ueye.is_InquireImageMem(self.hCam, self.pcImageMemory, self.MemID,
                                     self.width, self.height, self.nBitsPerPixel, self.pitch)
        if rc != ueye.IS_SUCCESS:
            return self._error("is_InquireImageMem ERROR")
        else:
            print("IDS camera: connection ok")
            self.ok = True

    def grab_image(self):
        if not self.ok:
            print("nicht ok")
            return None
        # In order to display the image in an OpenCV window we need to...
        # ...extract the data of our image memory
        array = ueye.get_data(self.pcImageMemory, self.width, self.height, self.nBitsPerPixel, self.pitch, copy=False)
        # ...reshape it in an numpy array...
        frame = np.reshape(array, (self.height.value, self.width.value, self.bytes_per_pixel))

        # ...resize the image by a half
        # frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)
        self.last_frame = frame
        return frame

    def disconnect(self):
        # Releases an image memory that was allocated using is_AllocImageMem() and removes it from the driver management
        ueye.is_FreeImageMem(self.hCam, self.pcImageMemory, self.MemID)

        # Disables the hCam camera handle and releases the data structures and memory areas taken up by the uEye camera
        ueye.is_ExitCamera(self.hCam)

    def set_camera_exposure(self, level_us):
        """
        :param level_us: exposure level in micro-seconds, or zero for auto exposure
        
        note that you can never exceed 1000000/fps, but it is possible to change the fps
        """
        p1 = ueye.DOUBLE()
        if level_us == 0:
            rc = IdsCamera._is_SetExposureTime(self.hCam, ueye.IS_SET_ENABLE_AUTO_SHUTTER, p1)
            print(f'set_camera_exposure: set to auto')
        else:
            ms = ueye.DOUBLE(level_us / 1000)
            rc = IdsCamera._is_SetExposureTime(self.hCam, ms, p1)
            print(f'set_camera_exposure: requested {ms.value}, got {p1.value}')

    def get_camera_exposure(self, force_val=False):
        """
        returns the current exposure time in micro-seconds, or zero if auto exposure is on

        :param force_val: if True, will return level of exposure even if auto exposure is on
        """
        p1 = ueye.DOUBLE()
        p2 = ueye.DOUBLE()
        # we dump both auto-gain and auto exposure states:
        rc = ueye.is_SetAutoParameter(self.hCam, ueye.IS_GET_ENABLE_AUTO_GAIN, p1, p2)
        print(f'IS_GET_ENABLE_AUTO_GAIN={p1.value == 1}')
        rc = ueye.is_SetAutoParameter(self.hCam, ueye.IS_GET_ENABLE_AUTO_SHUTTER, p1, p2)
        print(f'IS_GET_ENABLE_AUTO_SHUTTER={p1.value == 1}')
        if (not force_val) and p1.value == 1:
            return 0  # auto exposure
        rc = IdsCamera._is_SetExposureTime(self.hCam, IdsCamera.IS_GET_EXPOSURE_TIME, p1)
        print(f'IS_GET_EXPOSURE_TIME={p1.value}')
        return p1.value * 1000