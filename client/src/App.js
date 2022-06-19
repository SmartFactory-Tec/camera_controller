import './App.css';
import {
    Heading,
    Main,
    Nav,
    Anchor,
    Sidebar,
    Box,
    Page,
    Image,
    Grid,
    Video,
    ResponsiveContext,
    Collapsible
} from "grommet";
import * as Icons from 'grommet-icons'
import {Routes, Route, Link, useMatch} from "react-router-dom";
import CameraOverview from "./components/CameraOverview";
import {useContext} from "react";

function App() {
    const matchRoot = useMatch('/');
    const matchCameras = useMatch('/cameras/*');
    const size = useContext(ResponsiveContext);
    return (<Box direction='row' height='100vh'>
        <Sidebar background="brand"
                 header={<Box direction='row' gap='small' align='center'><Icons.Cubes/><Heading level={3} margin='none'>Smart
                     Factory</Heading></Box>}
                 pad={{horizontal: 'medium', vertical: 'large'}}>
            <Nav direction='column'>
                <Anchor icon={<Icons.Home/>} as={Link} to='/' label={"Camaras"}/>
                <Collapsible open={matchRoot || matchCameras}>
                    <Nav direction='column'>
                        <Anchor label='Camara 1' icon={<Icons.Video/>} margin={{left: 'medium'}} as={Link}
                                to='/cameras/cam1'/>
                        <Anchor label='Camara 2' icon={<Icons.Video/>} margin={{left: 'medium'}} as={Link}
                                to='/cameras/cam2'/>
                        <Anchor label='Camara 3' icon={<Icons.Video/>} margin={{left: 'medium'}} as={Link}
                                to='/cameras/cam3'/>
                        <Anchor label='Camara 4' icon={<Icons.Video/>} margin={{left: 'medium'}} as={Link}
                                to='/cameras/cam4'/>
                    </Nav>
                </Collapsible>
                <Anchor icon={<Icons.SettingsOption/>} as={Link} to='/settings' label={"Configuración"}/>
            </Nav>
        </Sidebar>
        <Main pad='large'>
            <Page>
                <Routes>
                    <Route path='/' element={<CameraOverview/>}/>
                </Routes>

            </Page>
        </Main>
    </Box>);
}

export default App;
