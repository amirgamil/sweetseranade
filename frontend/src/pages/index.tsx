import Head from "next/head";
import * as React from "react";
import FlowerTop from "../../public/flowers.png";
import styles from "@/styles/Home.module.css";
import { SeparateImage } from "../components/SeparateImage";
import { FileInput } from "../components/FileInput";
import { Button } from "../components/Button";
import { Typewriter } from "react-simple-typewriter";
import { useWindowSize } from "../hooks/useWindowSize";
import { Input } from "../components/Input";
import { API_ENDPOINT, loadingTextOptions } from "../utils/constants";
import toast, { Toaster } from "react-hot-toast";
import axios, { isAxiosError } from "axios";

export default function Home() {
    const [characterFirst, setCharacterFirst] = React.useState("");
    const [characterSecond, setCharacterSecond] = React.useState("");
    const [openaiKey, setOpenaiKey] = React.useState("");
    const [fileName, setFileName] = React.useState<string>("");
    const [loadingText, setLoadingText] = React.useState<string | undefined>(undefined);
    const size = useWindowSize();
    const [style, setStyle] = React.useState("");
    const [generatedSong, setGeneratedSong] = React.useState("");
    const [errorMessage, setErrorMesage] = React.useState("");

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
        if (!loadingText) {
            setLoadingText(loadingTextOptions[0]);
            setErrorMesage("");
            let updateLoading: NodeJS.Timer | undefined = undefined;
            try {
                updateLoading = setInterval(
                    ((counter: number) => () => {
                        counter = (counter + 1) % loadingTextOptions.length;
                        setLoadingText(loadingTextOptions[counter]);
                    })(0),
                    2000
                );
                const formData = new FormData();
                const headers = {
                    accept: "application/json",
                    "Content-Type": "multipart/form-data",
                };
                formData.append("file", fileRef.current![0], "file");
                const axiosResponse = await axios.post(API_ENDPOINT, formData, {
                    headers: headers,
                    params: {
                        character_first: characterFirst,
                        character_second: characterSecond,
                        style: style,
                        openai_api_key: openaiKey,
                    },
                });
                if (axiosResponse.status != 200) {
                    if (axiosResponse.data.detail === "File too large, please pass in OpenAI key") {
                        setErrorMesage("Sorry, for large documents please pass in your OpenAI key!");
                    } else {
                        setErrorMesage(
                            "Sorry, we ran into an issue. It's likely we ran out of our OpenAI credits or are being rate limited. Try passing in your own key!"
                        );
                    }
                    setLoadingText(undefined);
                    clearInterval(updateLoading);
                }
                setGeneratedSong(axiosResponse.data.completion);
                setLoadingText(undefined);
                // Reset the error message
                setErrorMesage("");
                clearInterval(updateLoading);
                toast.success("Song generated! Scroll down to see your song!");
            } catch (ex: unknown) {
                if (isAxiosError(ex)) {
                    if (ex && ex?.response?.data.detail === "File too large, please pass in OpenAI key") {
                        setErrorMesage("Sorry, for large documents please pass in your OpenAI key");
                    } else {
                        setErrorMesage(
                            "Sorry, we ran into an issue. It's likely we ran out of our OpenAI credits or are being rate limited. Try passing in your own key!"
                        );
                    }
                } else {
                    setErrorMesage(
                        "Sorry, we ran into an issue. It's likely we ran out of our OpenAI credits or are being rate limited. Try passing in your own key!"
                    );
                }
                setLoadingText(undefined);
                clearInterval(updateLoading);
            }
        }
    };

    return (
        <div className={styles.container}>
            <Head>
                <title>Sweet Serenade</title>
                <meta name="SweetSerenade" content="Generate a love poem from a PDF" />
                <link rel="icon" href="/rose.jpg" />
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
                        <Input
                            placeholder="OpenAI Key (for documents over 50kB)"
                            value={openaiKey}
                            onChange={setOpenaiKey}
                            password={true}
                        />
                        <div className="py-2"></div>
                        <Input placeholder="Character 1" value={characterFirst} onChange={setCharacterFirst} />
                        <div className="py-2"></div>
                        <Input placeholder="Character 2" value={characterSecond} onChange={setCharacterSecond} />
                        <div className="py-2"></div>
                        <Input placeholder="Style" value={style} onChange={setStyle} />
                        <div className="py-4"></div>
                        {errorMessage && (
                            <div className="text-red-500 text-center font-sans text-lg pb-4">
                                {errorMessage}{" "}
                                {!errorMessage.startsWith("Sorry, for")
                                    ? "To keep this project running for free, feel free to donate here"
                                    : ""}{" "}
                                <a
                                    className="text-green-600"
                                    href="https://etherscan.io/address/0xaecac2b465c6135be357095cd220309622d41517"
                                    target="_blank"
                                    rel="noreferrer"
                                >
                                    verumlotus.eth
                                </a>
                            </div>
                        )}
                        {loadingText ? (
                            <p className="text-center">{loadingText}</p>
                        ) : (
                            <Button onClick={generateSong}>Generate song</Button>
                        )}
                    </div>
                )}
                <div className="py-4"></div>
                {generatedSong && <div className={styles.song}>{generatedSong}</div>}
                <footer className={styles.footer}>
                    Built by{" "}
                    <a href="https://twitter.com/amirbolous" target="_blank" rel="noreferrer">
                        Amir
                    </a>{" "}
                    and{" "}
                    <a href="https://twitter.com/verumlotus" target="_blank" rel="noreferrer">
                        Verumlotus
                    </a>{" "}
                    and{" "}
                    <a href="https://github.com/amirgamil/sweetseranade" target="_blank" rel="noreferrer">
                        open source
                    </a>{" "}
                    on Github
                </footer>
                <Toaster />
            </main>
        </div>
    );
}
