import axios from "axios";

// TODO: Load from .env
export const BASE_URL = "http://localhost:8001/api";

// TODO: Implement login workflow
export const AUTHORIZATION_HEADER =
  "Token a10adb976f48276e3daaa6294086fb79ef4e30c5";

export const GetUsersFiles = async () => {
  try {
    const response = await axios.get(BASE_URL + "/file_versions/", {
      headers: {
        Authorization: AUTHORIZATION_HEADER,
      },
    });

    if (response.status === 200) {
      return response.data;
    } else {
      // TODO: Handle error
      return [];
    }
  } catch (error) {
    // TODO: Handle error
    console.log(error);
  }
};

export const UploadFile = async (filePath, file) => {
  try {
    const headers = {
      Authorization: AUTHORIZATION_HEADER,
      "X-File-Path": filePath,
      "Content-Type": "multipart/form-data",
    };

    let formData = new FormData();
    formData.append("file", file);
    const response = await axios.post(BASE_URL + "/file_versions/", formData, {
      headers: headers,
    });

    if (response.status === 201) {
      return response.data;
    } else {
      console.log(response);
    }
  } catch (error) {
    // TODO: Handle error
    console.log(error);
  }
};

export const DownloadFile = async (fileVersion) => {
  console.log(fileVersion);

  const { path, version_number, file_name } = fileVersion;
  try {
    const response = await axios.get(
      BASE_URL + "/file_versions/" + path + "?revision=" + version_number,
      {
        headers: {
          Authorization: AUTHORIZATION_HEADER,
        },
      },
    );

    if (response.status === 200) {
      const file = new Blob([response.data], {
        type: fileVersion.content_type,
      });
      const href = URL.createObjectURL(file);
      const link = document.createElement("a");
      link.href = href;
      link.setAttribute("download", file_name);
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      URL.revokeObjectURL(href);
    } else {
      // TODO: Handle error
      console.log(response);
    }
  } catch (error) {
    // TODO: Handle error
    console.log(error);
  }
};
