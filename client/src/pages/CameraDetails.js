import React from "react";
import {Page} from "grommet";
import {PageHeader} from "grommet/components";
import {useMatch} from 'react-router-dom';
import PropTypes from "prop-types";

export default function CameraDetails(props) {
    const match = useMatch();
    return <Page>
        <PageHeader title={props.slug}/>
    </Page>
}

CameraDetails.propTypes = {
    cameras: PropTypes.objectOf(PropTypes.string),
}