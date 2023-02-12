import styled from "styled-components";

const Container = styled.div`
    font-family: "Tajawal", sans-serif;
    input {
        padding: 0.3rem 0.5rem;
        width: 100%;
    }
`;

interface Props {
    placeholder: string;
    value: string;
    onChange: (newVal: string) => void;
}

export const Input = ({ placeholder, value, onChange }: Props) => {
    return (
        <Container className="w-full">
            <input
                className="w-full"
                placeholder={placeholder}
                value={value}
                onChange={(evt) => onChange(evt.target.value)}
            />
        </Container>
    );
};
