import React from "react";
import CameraView from "./CameraView";
import {Grid, Page} from "grommet";
import {PageHeader} from "grommet/components";
import Cameras from "./Cameras";

export default function CameraOverview() {
    return <Page>
        <PageHeader
            title='Sistema de camaras de seguridad'
            subtitle="Smart Factory"/>
        <Cameras/>
        <Grid
            fill='horizontal'
            columns={{count: 'fill', size: '1/2'}}
            gap={{
                column: "large", row: "small",
            }}
        >
            <CameraView cameraName='Camera 1'
                        slug='cam1'
                        streamSource='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
            <CameraView cameraName='Camera 2'
                        slug='cam2'
                        streamSource='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
            <CameraView cameraName='Camera 3'
                        slug='cam3'
                        streamSource='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
            <CameraView cameraName='Camera 4'
                        slug='cam4'
                        streamSource='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
        </Grid>
    </Page>
}