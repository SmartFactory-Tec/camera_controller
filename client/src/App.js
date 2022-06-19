import './App.css';
import {Header, Main, Nav, Anchor, Sidebar, Box, Page, Image, Grid, Video, ResponsiveContext} from "grommet";
import * as Icons from 'grommet-icons'
import {Link} from "react-router-dom";
import {PageHeader} from "grommet/components";
import Cameras from "./components/Cameras";

function App() {
    return (<Box direction='row' height='100vh'>
        <Sidebar background="brand"
                 header={<Icons.Video/>} pad={{horizontal: 'medium', vertical: 'large'}}>
        </Sidebar>
        <Main pad='large'>
            <Page>
                <PageHeader
                    title='Video de seguridad en vivo'
                    subtitle="Sistema de Camaras de Smart Factory"/>
                <Cameras/>
            </Page>
        </Main>
    </Box>);
}

export default App;
