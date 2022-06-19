import React from "react";
import {ResponsiveContext, Tabs, Tab, Box, Image, Grid} from "grommet";
import CameraView from "./CameraView";

export default function Cameras() {

    const size = React.useContext(ResponsiveContext);

    if (size === 'small') {
        return <Box>
        </Box>
    } else {
        return
    }
}