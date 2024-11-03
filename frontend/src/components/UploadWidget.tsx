import { useEffect, useRef } from "react";
import { Dispatch, SetStateAction } from "react";

interface UploadWidgetProps {
  setImageId: Dispatch<SetStateAction<string>>;
}

function UploadWidget({ setImageId }: UploadWidgetProps) {
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
          setImageId(result.info.public_id);
        }
      }
    );
  }, [setImageId]);

  return (
    <>
      <button type="button" onClick={() => widgetRef.current.open()}>
        Upload
      </button>
    </>
  );
}
export default UploadWidget;
