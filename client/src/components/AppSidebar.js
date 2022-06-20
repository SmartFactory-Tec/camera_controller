import {Link, useMatch} from "react-router-dom";
import {Anchor, Box, Collapsible, Heading, Nav, Sidebar} from "grommet";
import * as Icons from "grommet-icons";

export function AppSidebar(props) {
    const matchRoot = useMatch('/');
    const matchCameras = useMatch('/cameras/*');
    const expandCameras = matchRoot || matchCameras;

    return <Sidebar background="brand"
                    header={<Box direction="row" gap="small" align="center"><Icons.Cubes/><Heading level={3}
                                                                                                   margin="none">Smart
                        Factory</Heading></Box>}
                    pad={{horizontal: "medium", vertical: "large"}}>
        <Nav direction="column">
            <Anchor icon={<Icons.Home/>} as={Link} to="/" label={"Camaras"}/>
        </Nav>
        <Collapsible open={expandCameras}>
            <Nav direction="column" margin={{top: "medium"}}>
                <Anchor label="Camara 1" icon={<Icons.Video/>} margin={{left: "medium"}} as={Link}
                        to="/cameras/cam1"/>
                <Anchor label="Camara 2" icon={<Icons.Video/>} margin={{left: "medium"}} as={Link}
                        to="/cameras/cam2"/>
                <Anchor label="Camara 3" icon={<Icons.Video/>} margin={{left: "medium"}} as={Link}
                        to="/cameras/cam3"/>
                <Anchor label="Camara 4" icon={<Icons.Video/>} margin={{left: "medium"}} as={Link}
                        to="/cameras/cam4"/>
            </Nav>
        </Collapsible>
        <Nav direction="column" margin={{top: "medium"}}>
            <Anchor icon={<Icons.SettingsOption/>} as={Link} to="/settings" label={"Configuración"}/>
        </Nav>
    </Sidebar>;
}