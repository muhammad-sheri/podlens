import axios from "axios";

// PodLens has no authentication — requests go straight to the API.
const client = axios.create({ baseURL: "/api" });

export default client;
