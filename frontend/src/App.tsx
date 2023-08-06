import ResponsiveAppBar from "./modules/TopMenu.tsx";
import { ThemeProvider, createTheme } from '@mui/material';


const theme = createTheme({
    palette: {
        primary: {
            main: "#6E0000"
        },
        secondary: {
            main: "#232323"
        },
    },
});

function funny() {
    (console.log("Hey, where are you looking?! My page is up here!"))
}
funny()

function App() {
  return (
    <ThemeProvider theme={theme}>
      <ResponsiveAppBar />
    </ThemeProvider>
)
}

export default App
