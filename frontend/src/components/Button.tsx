import styled from "styled-components";

const Container = styled.div<{ fgColor: string; bgColor: string }>`
    button {
        border: 1px solid #f0adb0d5 !important;
        color: ${(props) => props.fgColor};
        z-index: 5;

        &:hover {
            background: #f0adb0d5;
            cursor: grab;
        }
    }
`;

interface Props {
    children?: any;
    fgColor?: string;
    bgColor?: string;
    className?: string;
    onClick: () => void;
}

export const Button = ({ children, onClick, fgColor = "white", bgColor = "transparent", className = "" }: Props) => {
    return (
        <Container fgColor={fgColor} bgColor={bgColor}>
            <button onClick={onClick} className={`${className}`}>
                {children}
            </button>
        </Container>
    );
};
