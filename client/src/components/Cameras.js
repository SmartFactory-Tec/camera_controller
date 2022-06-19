import React from "react";
import {ResponsiveContext, Tabs, Tab, Box, Image, Grid} from "grommet";

export default function Cameras() {

    const size = React.useContext(ResponsiveContext);

    if (size === 'small') {
        return <Tabs alignControls='start'>
            <Tab title='Camera 1'>
                <Box pad='large'>
                    <Image
                        src='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
                </Box>
            </Tab>
            <Tab title='Camera 2'>
                <Box pad='large'>
                    <Image
                        src='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
                </Box>
            </Tab>
        </Tabs>
    } else {
        return <Grid
            fill='horizontal'
            columns={{count: 'fill', size:'1/2'}}
            rows='large'
            gap={{
                column: "large",
                row: "small",
            }}
        >
            <Box>
                <Image
                    src='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
            </Box>
            <Box>
                <Image
                    src='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
            </Box>
            <Box>
                <Image
                    src='https://ie.trafficland.com/v2.0/200123/full?system=ddot&pubtoken=51662654cdfaead409679af69261a92adbf20e0467fa760e345d7cd2025354a9&refreshRate=2000&t=1655665339153'/>
            </Box>
            <Box>
                <Image
                    src='https://ie.trafficland.com/v2.0/200127/full?system=ddot&pubtoken=cc9e66f592ad327c8fec37c2c94c8bddee14bbb8653546a23507cdb4aefa9cd3&refreshRate=2000&t=1655665788013'/>
            </Box>
        </Grid>
    }
}