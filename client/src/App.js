import './App.css';
import {Box, Main, Page} from "grommet";
import {Route, Routes} from "react-router-dom";
import CameraOverview from "./pages/CameraOverview";
import CameraDetails from "./pages/CameraDetails";
import * as PropTypes from "prop-types";
import {AppSidebar} from "./components/AppSidebar";

AppSidebar.propTypes = {open: PropTypes.any};

function App() {

    return (<Box direction='row' height='100vh'>
        <AppSidebar/>
        <Main pad='large'>
            <Routes>
                <Route path='/' element={<CameraOverview/>}/>
                <Route path='/camera/:slug' element={<CameraDetails/>}/>
            </Routes>
        </Main>
    </Box>);
}

export default App;
