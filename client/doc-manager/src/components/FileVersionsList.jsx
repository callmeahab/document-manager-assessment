import React from "react";
import { DownloadFile } from "../utils";

function FileVersionsList(props) {
  const file_versions = props.file_versions;
  return file_versions.map((file_version) => (
    <div
      className="flex align-middle border-2 border-slate-600 bg-slate-800 rounded-lg px-4 py-6 mb-2"
      key={file_version.id}
    >
      <div className="flex-1 my-auto h-full">
        <h2>File Path: {file_version.path}</h2>
        <p>
          ID: {file_version.id} Version: {file_version.version_number}
        </p>
      </div>
      <div className="my-auto h-full">
        <button
          type="button"
          className="px-4 py-2.5 mx-auto block text-sm bg-blue-500 text-white rounded transition ease-in-out duration-200 hover:bg-blue-600"
          onClick={async () => {
            await DownloadFile(file_version);
          }}
        >
          Download file
        </button>
      </div>
    </div>
  ));
}

export default FileVersionsList;
