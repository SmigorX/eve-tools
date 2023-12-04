import {Button} from "@mui/material";

export default function MainPage() {
    return (
        <div>
        <div style={{
            display: "grid",
                gridTemplateColumns: "repeat(2, 1fr)",
                gap: "10px",
                maxWidth: "500px",
                margin: "50px",
                marginLeft: "40.7%",
                width: "1px"
            }}>
                {NavigationButton("api", "/api")}
                {NavigationButton("categories", "/categories")}
                {NavigationButton("products", "/products")}
                {NavigationButton("root", "/")}
            </div>
        </div>
    )
}

const NavigationButton = (button_text, button_link) => {
    return (
        <Button
            href={button_link}
            variant="contained"
            style={{
            backgroundColor: "#BB7744",
            height: "30mm",
            width: "60mm",
            borderRadius: "20px",
        }}>
            {button_text}
        </Button>
    )
}
