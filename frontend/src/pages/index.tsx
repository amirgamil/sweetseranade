import Head from "next/head";
import * as React from "react";
import { Inter } from "@next/font/google";
import FlowerTop from "../../public/flowers.png";
import styles from "@/styles/Home.module.css";
import { SeparateImage } from "../components/SeparateImage";
import { FileInput } from "../components/FileInput";
import { Button } from "../components/Button";

const inter = Inter({ subsets: ["latin"] });

export default function Home() {
    const [characterFirst, setCharacterFirst] = React.useState("");
    const [characterSecond, setCharacterSecond] = React.useState("");
    const [fileName, setFileName] = React.useState<string>("");
    const [style, setStyle] = React.useState("");

    const fileRef = React.useRef<FileList | null>(null);
    console.log(fileRef.current);
    return (
        <div className={styles.container}>
            <Head>
                <title>Sweet Serenade</title>
                <meta name="description" content="Generated by create next app" />
                <link rel="icon" href="/favicon.ico" />
            </Head>

            <div className="w-full flex justify-center items-center">
                <SeparateImage image={FlowerTop} alt="Flowers" width={1391} height={287} className="top-0 " />
            </div>
            <main className={styles.main}>
                <h1 className={styles.title}>️Sweet Serenade</h1>
                <p className="text-center text-lg">
                    Generate love songs between characters in a book, article, or literally anything you can turn into a
                    PDF document
                </p>

                <div className="py-4"></div>

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
                {fileName && (
                    <div>
                        <div className="py-2"></div>
                        <p className="text-center text-lg">File: {fileName}</p>
                    </div>
                )}
                <div className="py-4"></div>
                <footer className={styles.footer}>
                    Built by <a href="https://twitter.com/amirbolous">Amir</a> and{" "}
                    <a href="https://twitter.com/verumlotus">verumlotus</a> and{" "}
                    <a href="https://github.com/amirgamil/zk-crush">open source</a> on Github
                </footer>
            </main>
        </div>
    );
}
