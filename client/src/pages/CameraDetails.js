import React, {useEffect, useState} from "react";
import {Image, Page, Grid, Box, Select, ResponsiveContext, CheckBox} from "grommet";
import {PageHeader} from "grommet/components";
import {useParams} from 'react-router-dom';
import PropTypes from "prop-types";

export default function CameraDetails(props) {
    const urlParams = useParams();

    const [res, setRes] = useState('480p');

    const [showDetections, setShowDetections] = useState(false);

    let feedSource = '/api/camera/' + urlParams.slug;

    if (showDetections) feedSource += '/detections';

    feedSource += '/video_feed?res=' + res.substring(0, res.length - 1)

    return <Page gap='medium'>
        <PageHeader title={urlParams.slug}/>
        <Box fill='horizontal'>
            <Image src={feedSource} fill alignSelf='start'/>
        </Box>
        <Box width='medium' gap='medium'>
            <Select
                options={['144p', '240p', '360p', '480p', '720p', '1080p']}
                value={res}
                onChange={({ option }) => setRes(option)}
            />
            <CheckBox
                checked={showDetections}
                label="Mostrar detecciones"
                onChange={(event) => setShowDetections(event.target.checked)}
            />
        </Box>
    </Page>
}