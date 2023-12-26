import {Button} from "@mui/material";

const buttons = [
    { name: 'api', link: '/api' },
    { name: 'categories', link: '/categories' },
    { name: 'products', link: '/products' },
    { name: 'root', link: '/' },
];

export default function MainPage() {
    return (
            <div
                style={{
                    display: 'grid',
                    gridTemplateColumns: 'auto auto',
                    gap: '10px',
                }}
            >
                {buttons.map((button, index) => (
                    <div
                        key={index}
                        style={{
                            justifySelf: index % 2 === 0 ? 'right' : 'left',
                        }}
                    >
                        {NavigationButton(button.name, button.link)}
                    </div>
                ))}
            </div>
    );
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
