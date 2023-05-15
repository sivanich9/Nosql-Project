import logo from "./logo.svg";
import "./App.css";
import { v4 as uuidv4 } from "uuid";

// supabase
import { createClient } from "@supabase/supabase-js";
import { useState } from "react";

// supabase credentials
const project_url = "https://pkwxbrxicmbncxgcblbv.supabase.co";
const supabase_api_key =
	"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InBrd3hicnhpY21ibmN4Z2NibGJ2Iiwicm9sZSI6ImFub24iLCJpYXQiOjE2ODQxNjEzMDksImV4cCI6MTk5OTczNzMwOX0.AlBih_pbLn3jhcPqp0o-a0CP-80nO02PD7lM4UtiVuA";

// supabase client
const supabase = createClient(project_url, supabase_api_key);






function App() {
	const [xmlfile, setXmlFile] = useState("");
	const [datafile, setDataFile] = useState("");
    const [formError, setFormError] = useState(null);

	// function to upload corresponding files
	async function uploadXMLFile(e) {
		const pigfile = e.target.files[0];
		const { data, error } = await supabase.storage
			.from("pig_storage")
			.upload(uuidv4() + ".xml", pigfile);
		if (error) {
			// Handle error
			console.error(error);
		} else {
			// Handle success
            setXmlFile(data.path);
            console.log(data);
            console.log(xmlfile);
			return data;
		}
	}

	async function uploadDataFile(e) {
		const pigfile = e.target.files[0];
		const { data, error } = await supabase.storage
			.from("pig_storage")
			.upload(uuidv4() + ".tsv", pigfile);
		if (error) {
			// Handle error
			console.error(error);
		} else {
			// Handle success
			setDataFile(data.path)
            console.log(datafile)
			return data;
		}
	}


    const handleSubmit = async (e) => {
		e.preventDefault();

		if (!xmlfile && !datafile) {
			setFormError("please fill in all the fields correctly");
			return;
		}

		// console.log(headline, description, genre);
		setXmlFile(null);
        setDataFile(null);
        setFormError(null);


        fetch("http://localhost:8000/ingest", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({
                xmlfilePath: xmlfile,
                datafilePath: datafile
			}),
		})
			.then((response) => response.json())
			.then((response) => {
				console.log(response);
			})
			.catch((err) => {
                console.error(err);                
			});
	};



	return (
		<div className="App">
			<header className="App-header">
				<form onSubmit={handleSubmit}>
					<label htmlFor="xmlfile">Choose XML ingestion</label>
					<input
						type="file"
						id="xmlfile"
						name="xmlfile"
						onChange={(e) => uploadXMLFile(e)}
					/>

					<span className="spanbreak"></span>

					<label htmlFor="datafile">
						Choose datafile for ingestion
					</label>
					<input
						type="file"
						id="datafile"
						name="datafile"
						onChange={(e) => uploadDataFile(e)}
					></input>

					<span className="spanbreak"></span>

                    {xmlfile && <p>{xmlfile}</p>}
                    {datafile && <p>{datafile}</p>}

					<button>Submit</button>
                    {formError && <p>{formError}</p>}
				</form>
			</header>
		</div>
	);
}

export default App;
