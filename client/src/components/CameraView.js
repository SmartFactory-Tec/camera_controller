import React from 'react';
import {Image, Box, Heading, Anchor, Button} from 'grommet';
import * as Icons from 'grommet-icons';
import {Link} from 'react-router-dom';
import PropTypes from 'prop-types';

export default function CameraView(props) {
    return <Box>
        <Image src={props.streamSource}/>
        <Box direction='row' justify='between'>
            <Heading level='2'>
                <Anchor label={props.cameraName}
                        as={Link}
                        to={'/cameras/' + props.slug}/>
            </Heading>
            <Button icon={<Icons.Expand/>} secondary></Button>
        </Box>
    </Box>
}

CameraView.propTypes = {
    cameraName: PropTypes.string.isRequired,
    slug: PropTypes.string.isRequired,
    streamSource: PropTypes.string.isRequired,
}