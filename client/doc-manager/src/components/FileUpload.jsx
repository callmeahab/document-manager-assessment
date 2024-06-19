import React, { useState } from "react";
import { UploadFile } from "../utils";

function FileUpload({ allFiles, setAllFiles }) {
  const [filePath, setFilePath] = useState("");
  const [selectedFile, setSelectedFile] = useState(null);

  const handleFileSelect = (event) => {
    const { files } = event.target;
    if (files.length) {
      setFilePath("/documents/" + files[0].name);
      setSelectedFile(files[0]);
    }
  };

  const handleFilePathChange = (event) => {
    setFilePath(event.target.value);
  };

  const uploadFile = async () => {
    const response = await UploadFile(filePath, selectedFile);
    if (response) {
      setAllFiles([...allFiles, response]);
    }
  };

  return (
    <div className="space-y-6">
      <label
        htmlFor="uploadFile1"
        className="bg-slate-800 text-slate-300 font-semibold text-base rounded max-w-md h-40 flex flex-col items-center justify-center cursor-pointer border-2 border-slate-600 border-dashed mx-auto font-[sans-serif]"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          className="w-11 mb-2 fill-slate-300"
          viewBox="0 0 32 32"
        >
          <path
            d="M23.75 11.044a7.99 7.99 0 0 0-15.5-.009A8 8 0 0 0 9 27h3a1 1 0 0 0 0-2H9a6 6 0 0 1-.035-12 1.038 1.038 0 0 0 1.1-.854 5.991 5.991 0 0 1 11.862 0A1.08 1.08 0 0 0 23 13a6 6 0 0 1 0 12h-3a1 1 0 0 0 0 2h3a8 8 0 0 0 .75-15.956z"
            data-original="#000000"
          />
          <path
            d="M20.293 19.707a1 1 0 0 0 1.414-1.414l-5-5a1 1 0 0 0-1.414 0l-5 5a1 1 0 0 0 1.414 1.414L15 16.414V29a1 1 0 0 0 2 0V16.414z"
            data-original="#000000"
          />
        </svg>
        Upload file
        <input
          type="file"
          id="uploadFile1"
          className="hidden"
          onChange={handleFileSelect}
        />
        <p className="text-xs font-medium text-slate-300 mt-2">
          All file types are allowed.
        </p>
      </label>

      <div className="flex rounded-md border-2 border-blue-500 overflow-hidden max-w-md mx-auto font-[sans-serif]">
        <input
          onChange={handleFilePathChange}
          value={filePath}
          type="email"
          placeholder="File destination path"
          className="w-full outline-none bg-slate-700 text-white text-sm px-4 py-3"
        />
      </div>

      <div>
        <button
          type="button"
          className="px-4 py-2.5 mx-auto block text-sm bg-blue-500 text-white rounded transition ease-in-out duration-200 hover:bg-blue-600"
          onClick={uploadFile}
        >
          Upload file
        </button>
      </div>
    </div>
  );
}

export default FileUpload;
