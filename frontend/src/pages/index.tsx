import Head from "next/head";
import * as React from "react";
import { Inter } from "@next/font/google";
import FlowerTop from "../../public/flowers.png";
import styles from "@/styles/Home.module.css";
import { SeparateImage } from "../components/SeparateImage";
import { FileInput } from "../components/FileInput";
import { Button } from "../components/Button";
import { Typewriter } from "react-simple-typewriter";
import { useWindowSize } from "../hooks/useWindowSize";
import { Input } from "../components/Input";
import { TEMPLATE_SONG } from "../utils/constants";

export default function Home() {
    const [characterFirst, setCharacterFirst] = React.useState("");
    const [characterSecond, setCharacterSecond] = React.useState("");
    const [fileName, setFileName] = React.useState<string>("");
    const size = useWindowSize();
    const [style, setStyle] = React.useState("");
    const [generatedSong, setGeneratedSong] = React.useState("");

    const fileRef = React.useRef<FileList | null>(null);
    const characters_first = React.useMemo(
        () => ["Harry", "Tom", "AI", "King Henry VII", "Napolean", "Seneca", "Shakespeare"],
        []
    );
    const characters_second = React.useMemo(
        () => ["Hermonie", "Jerry", "human", "Catherine Par", "France", "Aristotle", "the pen"],
        []
    );
    const song_styles = React.useMemo(
        () => [
            "heavy metal rock",
            "a pop cover by Taylor Swift",
            "a rap from 8 mile",
            "a classic country song",
            "a traditional reggae song",
        ],
        []
    );

    const generateSong = async () => {
        //TODO: fetch actual song
        setGeneratedSong(TEMPLATE_SONG);
    };

    return (
        <div className={styles.container}>
            <Head>
                <title>Sweet Serenade</title>
                <meta name="description" content="Generated by create next app" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <div
                style={{ height: size && size.height && size.height > 400 ? "287px" : "200px" }}
                className="w-full flex justify-center items-center"
            >
                <SeparateImage image={FlowerTop} alt="Flowers" width={1391} height={287} className="top-0 z-0" />
            </div>
            <main className={styles.main}>
                <h1 className={styles.title}>️Sweet Serenade</h1>
                <div className="text-center text-lg" style={{ width: "400px" }}>
                    <i>
                        Generate love songs between characters in a book, article, or literally anything you can turn
                        into a PDF document.
                    </i>
                </div>

                <div className="py-4"></div>

                <div className="text-center text-lg" style={{ width: "400px" }}>
                    Write a song about{" "}
                    <span className="pink">
                        {fileRef.current ? (
                            characterFirst || "character 1"
                        ) : (
                            <Typewriter
                                typeSpeed={150}
                                deleteSpeed={40}
                                delaySpeed={5000}
                                words={characters_first}
                                loop={true}
                            ></Typewriter>
                        )}{" "}
                    </span>
                    and{" "}
                    <span className="pink">
                        {fileRef.current ? (
                            characterSecond || "character 2"
                        ) : (
                            <Typewriter
                                typeSpeed={120}
                                deleteSpeed={40}
                                delaySpeed={4900}
                                words={characters_second}
                                loop={true}
                            ></Typewriter>
                        )}{" "}
                    </span>{" "}
                    in the style of{" "}
                    <span className="pink">
                        {fileRef.current ? (
                            style || "style"
                        ) : (
                            <Typewriter
                                typeSpeed={100}
                                deleteSpeed={40}
                                delaySpeed={2000}
                                words={song_styles}
                                loop={true}
                            ></Typewriter>
                        )}
                    </span>
                </div>
                <div className="py-2"></div>
                {fileName ? (
                    <div className="w-full flex flex-row justify-around items-center">
                        <p className="text-center text-lg">File: {fileName}</p>
                        <FileInput
                            name="first"
                            accept=".pdf"
                            id="pdf"
                            onChange={(file) => {
                                fileRef.current = file;
                                setFileName(file?.[0].name || "");
                            }}
                        >
                            <Button onClick={() => document.getElementById("pdf")?.click()}>Upload</Button>
                        </FileInput>
                    </div>
                ) : (
                    <FileInput
                        name="first"
                        accept=".pdf"
                        id="pdf"
                        onChange={(file) => {
                            fileRef.current = file;
                            setFileName(file?.[0].name || "");
                        }}
                    >
                        <Button onClick={() => document.getElementById("pdf")?.click()}>Upload</Button>
                    </FileInput>
                )}
                <div className="py-2"></div>
                {fileName && (
                    <div className="w-full px-20 flex flex-col justify-center items-center">
                        <div className="py-2"></div>
                        <Input placeholder="Character 1" value={characterFirst} onChange={setCharacterFirst} />
                        <div className="py-2"></div>
                        <Input placeholder="Character 2" value={characterSecond} onChange={setCharacterSecond} />
                        <div className="py-2"></div>
                        <Input placeholder="Style" value={style} onChange={setStyle} />
                        <div className="py-4"></div>
                        <Button onClick={generateSong}>Generate song</Button>
                    </div>
                )}
                <div className="py-4"></div>
                {generatedSong && <div className={styles.song}>{generatedSong}</div>}
                <footer className={styles.footer}>
                    Built by <a href="https://twitter.com/amirbolous">Amir</a> and{" "}
                    <a href="https://twitter.com/verumlotus">Verumlotus</a> and{" "}
                    <a href="https://github.com/amirgamil/zk-crush">open source</a> on Github
                </footer>
            </main>
        </div>
    );
}
