from arduinoConnector import ArduinoConnector
from camera import Camera
from processedImage import ProcessedImage
from display import Display
from variables import ArduinoVar, DisplayVar, ButtonVar, ImageVar
from gpiozero import Button
from datetime import datetime


class MainUI:
    cam = Camera()
    statusbutton = Button(ButtonVar.buttonpin)


    def __init__(self) -> None:
        #---------------UI layers
        self.stationaryOverlay = self.cam.getCam().add_overlay(self.getStationaryIM().tobytes(),
                                                 layer=3)
        self.movingOverlay = self.cam.getCam().add_overlay(self.getMovingIM().tobytes(),
                                                layer=4)
        ##Battery and highbeams images
        self.indicatorsOverlay = self.cam.getCam().add_overlay(self.getIndicatorIM().tobytes(),
                                                    layer=4)
        ##Time stamp overlay
        self.timeOverlay = self.cam.getCam().add_overlay(self.getTimeIM().tobytes(),
                                              layer=4)
        #-------------Button Var
        self.dataToButton = {'status':True, 'time':0}
        self.lights = True
        self.motors = False
        self.imagesDict = {"warning.png": None, "lowbatt.png": None,
                      "sub.png":None, "highbeams.png": None}
        self.arduino = ArduinoConnector()

    def getStationaryIM(self) -> Display:
        """Create the layer that is staionary. Contains info about
        yaw pitch, rpm, speed, depth, and all that
        """
        stationaryLayer = Display()
        stationaryLayer.drawRectangle(0,0,DisplayVar.screenX,
                                    DisplayVar.linegap*2.5, DisplayVar.background)
        stationaryLayer.drawRectangle(DisplayVar.screenX-DisplayVar.linegap*2.5,0,
                                    DisplayVar.screenX, DisplayVar.screenY, 
                                    DisplayVar.background)
        stationaryLayer.drawRectangle(DisplayVar.screenX*0, DisplayVar.screenY-DisplayVar.linegap*2,
                                    DisplayVar.screenX*1, DisplayVar.screenY, DisplayVar.background)
        stationaryLayer.drawLine(DisplayVar.linegap+DisplayVar.lineextra,DisplayVar.linegap,
                                DisplayVar.screenX-(DisplayVar.linegap+DisplayVar.lineextra),
                                DisplayVar.linegap, fill=DisplayVar.barcolor, width=DisplayVar.linewidth)
        stationaryLayer.drawLine(DisplayVar.screenX-(DisplayVar.linegap), DisplayVar.linegap+DisplayVar.lineextra,
                                DisplayVar.screenX-(DisplayVar.linegap), DisplayVar.screenY-DisplayVar.linegap-DisplayVar.lineextra, 
                                fill=DisplayVar.barcolor, width=DisplayVar.linewidth)
        stationaryLayer.drawLine(DisplayVar.screenX/2 ,DisplayVar.linegap*0.5, DisplayVar.screenX/2,
                                DisplayVar.linegap*1.5,fill=DisplayVar.barcolor, width=DisplayVar.linewidth)
        stationaryLayer.drawLine(DisplayVar.screenX-DisplayVar.linegap*1.5, DisplayVar.screenY/2,
                                DisplayVar.screenX-DisplayVar.linegap*0.5, DisplayVar.screenY/2,
                                fill=DisplayVar.barcolor, width=DisplayVar.linewidth)
        stationaryLayer.drawSmallText(DisplayVar.screenX*0.5-8*1, DisplayVar.linegap*2, "yaw",
                                fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.screenY*0.5-9*2, "p",
                                fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.screenY*0.5-9*1, "i",
                                fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.screenY*0.5, "t",
                                fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.screenY*0.5+9, "c",
                                fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.screenY*0.5+9*2, "h",
                                fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.linegap*2,
                                str(DisplayVar.pitchRange), fill=DisplayVar.barcolor)
        stationaryLayer.drawSmallText(DisplayVar.screenX-DisplayVar.linegap*2, DisplayVar.screenY-DisplayVar.linegap*2,
                                "-"+str(DisplayVar.pitchRange), fill=DisplayVar.barcolor)
        return stationaryLayer


    def updateUIUsingData(movinIM):
        movinIM.drawLine()
        movinIM.drawLine([yawAjust*screenX,linegap*0.5,yawAjust*screenX,linegap*1.5],fill = slidercolor, width=sliderwidth)
        movinIM.drawLine([screenX-linegap*1.5,screenY*pitchAjust,screenX-linegap*0.5,screenY*pitchAjust],fill = slidercolor, width=sliderwidth)
        movinIM.drawLine([screenX*0.3,screenY-linegap*1.5],ValuesText,fill=slidercolor,font=datafont,alin="center")

    def loadProcessedImages(self):
        # Images that we will use
        images = ["warning.png", "lowbatt.png",
                  "sub.png", "highbeams.png"]
        # Init images and store in dict
        self.imagesDict = {img.split("", 1)[0]: ProcessedImage(img) for img in images}


    def getMovingIM(self):
        return Display()

    def getIndicatorIM(self):
        return Display()

    def getTimeIM(self):
        return Display()

    def checkSwitchStatus(self):
        if self.statusbutton.is_pressed:
            indicatorIM = self.getIndicatorIM()
            if self.dataToButton['status'] == self.lights:
                self.dataToButton['status'] = self.motors
                indicatorIM = indicatorIM.paste(self.imagesDict['sub.png'],
                                                           [int(ImageVar.linegap*8),
                                                           int(DisplayVar.screenY-2*DisplayVar.linegap)]
                                                           )
                timestamp = datetime.now().strftime("%Y-%m-%d_%H_%M_%p")
                print("Start Recording")
                self.cam.getCam().start_recording(ArduinoVar.usbPath+timestamp+'.h264')
                self.cam.changeLedStatus(False)
                # save the time the recording starts
                self.dataToButton['time'] = int(self.cam.getCam().timestamp)
            else: 
                #change overlay status
                self.dataToButton['status'] = self.lights
                indicatorIM.paste(self.imagesDict['highbeams.png'],
                                  [int(DisplayVar.linegap*8),
                                  int(DisplayVar.screenY-2*DisplayVar.linegap)])
                #recoring stop
                self.cam.getCam().stop_recording()
                print("Stop Recording")
                self.cam.changeLedStatus(True)
                #clear the timestamp
                self.dataToButton['time'] = int(self.cam.getCam().timestamp)

            #update overlay
            self.cam.getCam().remove_overlay(self.indicatorsoverlay)
            self.indicatorsoverlay = self.cam.getCam().camera.add_overlay(self.indicatorsIM.tobytes(), layer=4)
            self.statusbutton.wait_for_release()

    def updateOverlays(self):
        flag = 0
        while flag < 1:
            DataToDisplay = self.arduino.readJsonFromArduino()
            # configure data Values to display
            ValuesText = ("RPM:" + str(DataToDisplay['rpm']) + " rpm    Speed:" + 
            str(DataToDisplay['speed']) + " m/s     Depth:" + str(DataToDisplay['depth']) + "m")
            pitchAjust = (DataToDisplay['pitch'] + DisplayVar.pitchRange) / (DisplayVar.pitchRange * 2)
            yawAjust = (DataToDisplay['yaw'] + DisplayVar.yawRange) / (DisplayVar.yawRange * 2)
            flag = 1

        ValuesText = ("RPM:"+str(DataToDisplay['rpm']) + " rpm    Speed:"+
                      str(DataToDisplay['speed']) + " m/s     Depth:"+
                      str(DataToDisplay['depth']) + "m")
        pitchAjust = (DataToDisplay['pitch'] + DisplayVar.pitchRange)/(DisplayVar.pitchRange*2)
        yawAjust = (DataToDisplay['yaw']+DisplayVar.yawRange)/(DisplayVar.yawRange*2)
        movingIM = self.getMovingIM()
        movingIM.drawDataLine(yawAjust*DisplayVar.screenX,DisplayVar.linegap*0.5,
                            yawAjust*DisplayVar.screenX,DisplayVar.linegap*1.5)
        movingIM.drawDataLine(DisplayVar.screenX-DisplayVar.linegap*1.5,
                               DisplayVar.screenY*pitchAjust,
                               DisplayVar.screenX-DisplayVar.linegap*0.5,
                               DisplayVar.screenY*pitchAjust)
        movingIM.drawDataText(DisplayVar.screenX*0.3,DisplayVar.screenY-DisplayVar.linegap*1.5,
                              ValuesText)

        if DataToDisplay['battery'] == True: 
            movingIM.paste(self.imagesDict["highbatt.png"],
                           [int(DisplayVar.linegap*4),
                           int(DisplayVar.screenY-2*DisplayVar.linegap)])

        self.movingOverlay.update(movingIM.tobytes())

    def startShowing(self):
        self.cam.getCam().start_preview()

def main():
    try:
        mainUI = MainUI()
        mainUI.startShowing()
        while True:
            mainUI.updateOverlays()
            mainUI.checkSwitchStatus()
            
    except KeyboardInterrupt:
        exit()
        
if __name__ == "__main__":
    main()
    
    
    
    