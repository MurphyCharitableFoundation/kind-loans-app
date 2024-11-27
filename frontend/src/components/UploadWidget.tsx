import { useEffect, useRef } from "react";
import { Dispatch, SetStateAction } from "react";
import { profileType } from "../pages/Profile/Profile";
import { preview } from "@cloudinary/url-gen/actions/videoEdit";

interface UploadWidgetProps {
  setImageId: Dispatch<SetStateAction<string>>;
  setProfileList: Dispatch<SetStateAction<profileType>>;
}

function UploadWidget({ setImageId, setProfileList }: UploadWidgetProps) {
  const cloudinaryRef = useRef();
  const widgetRef = useRef();

  useEffect(() => {
    cloudinaryRef.current = window.cloudinary;
    widgetRef.current = cloudinaryRef.current.createUploadWidget(
      {
        cloudName: "dqlx6iqqt",
        uploadPreset: "kind-loans-preset",
        multiple: false,
        sources: ["local", "camera"],
      },
      function (error: any, result: any) {
        if (!error && result && result.event === "success") {
          console.log(result.info);
          setImageId(result.info.secure_url);
          setProfileList((prev: profileType) => {
            return { ...prev, photoURL: result.info.public_id };
          });
        }
      }
    );
  }, [setImageId]);

  return (
    <>
      <button type="button" onClick={() => widgetRef.current.open()}>
        Add Photo
      </button>
    </>
  );
}
export default UploadWidget;
