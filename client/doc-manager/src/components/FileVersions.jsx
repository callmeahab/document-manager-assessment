import React, { useEffect, useState } from "react";

import FileVersionsList from "./FileVersionsList";
import { GetUsersFiles } from "../utils";
import FileUpload from "./FileUpload";

function FileVersions() {
  const [allFiles, setAllFiles] = useState([]);

  useEffect(() => {
    GetUsersFiles().then((response) => {
      setAllFiles(response);
    });
  }, []);

  return (
    <div>
      <div className="pb-4">
        <FileUpload allFiles={allFiles} setAllFiles={setAllFiles} />
      </div>

      <h1 className="text-2xl font-semibold pb-4 text-slate-200">
        Found {allFiles.length} File Versions
      </h1>
      <div>
        <FileVersionsList file_versions={allFiles} />
      </div>
    </div>
  );
}

export default FileVersions;
