import * as dotenv from "dotenv";
dotenv.config({ path: ".env" });

const API_KEY = process.env.API_KEY;

class NeoInterface {
  async getObjects() {
    const ENDPOINT = "feed?start_date=2025-08-20&end_date=2025-08-21&api_key=";
    const URI = `${process.env.BASE_URI}${ENDPOINT}${API_KEY}`;

    console.log("URI:",URI);
  }

  async getNames(near_earth_objects : string) {
    
  }
}

export default new NeoInterface();
