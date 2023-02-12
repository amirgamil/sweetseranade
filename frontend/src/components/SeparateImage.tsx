import Image, { StaticImageData } from "next/image";

export const SeparateImage = ({
    image,
    alt,
    width,
    height,
    className,
}: {
    image: StaticImageData;
    alt: string;
    width: number;
    height: number;
    className?: string;
}) => {
    return (
        <div className={`absolute ${className ? className : ""}`}>
            <Image src={image} alt={alt} width={width} height={height} />
        </div>
    );
};
