// import needed deps
import e from "express";
import NeoInterface from "./NeoInterfaceLib/NeoInterfaceLib.ts"

const app = e();

app.get("/NearEarthObjects", (req,res) => {
    NeoInterface.getObjects();
});

app.listen(8080, () => {
    console.log("Listening on port 8080");
});