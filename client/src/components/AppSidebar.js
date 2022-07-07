import {Link, useMatch} from "react-router-dom";
import {Anchor, Box, Collapsible, Heading, Nav, Sidebar} from "grommet";
import * as Icons from "grommet-icons";
import {useQuery} from "react-query";
import {getCameraListing} from "../api/cameras";

export function AppSidebar(props) {
    const matchRoot = useMatch('/');
    const matchCameras = useMatch('/camera/*');
    const expandCameras = matchRoot === null || matchCameras === null;

    const {isLoading, isError, data, error} = useQuery('cameras', getCameraListing);

    return <Sidebar background="brand"
                    header={<Box direction="row" gap="small" align="center"><Icons.Cubes/><Heading level={3}
                                                                                                   margin="none">Smart
                        Factory</Heading></Box>}
                    pad={{horizontal: "medium", vertical: "large"}}>
        <Nav direction="column">
            <Anchor icon={<Icons.Home/>} as={Link} to="/" label={"Camaras"}/>
        </Nav>
        <Collapsible open={expandCameras && !isLoading && !isError}>
            <Nav direction="column" margin={{top: "medium"}}>
                { data ?
                    data.body.map((cameraInfo) => {
                        return <Anchor label={cameraInfo.name} icon={<Icons.Video/>} margin={{left: "medium"}} as={Link}
                        to={"/camera/" + cameraInfo.slug}/>
                    }) : null
                }
            </Nav>
        </Collapsible>
        <Nav direction="column" margin={{top: "medium"}}>
            <Anchor icon={<Icons.SettingsOption/>} as={Link} to="/settings" label={"Configuración"}/>
        </Nav>
    </Sidebar>;
}