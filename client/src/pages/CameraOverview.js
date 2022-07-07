import React, {useState} from "react";
import CameraView from "../components/CameraView";
import {Grid, Page, Box, Spinner} from "grommet";
import {PageHeader} from "grommet/components";
import Cameras from "../components/Cameras";
import {useQuery} from "react-query";
import {getCameraListing} from "../api/cameras";

export default function CameraOverview() {
    const {isLoading, isError, data, error} = useQuery('cameras', getCameraListing);

    return <Page>
        <PageHeader
            title='Sistema de camaras de seguridad'
            subtitle="Smart Factory"/>
        <Cameras/>
        {
            isLoading ?
                <Box>
                    <Spinner size='xlarge'/>
                </Box> :
                <Grid fill='horizontal'
                      columns={{count: 'fill', size: '1/2'}}
                      gap={{
                          column: "large", row: "small",
                      }}>
                    {
                        data.body.map((cameraInfo) => {
                            return <CameraView cameraName={cameraInfo.name} slug={cameraInfo.slug}
                                               streamSource={'/api/camera/' + cameraInfo.slug + '/video_feed'}/>
                        })
                    }
                </Grid>
        }
    </Page>
}