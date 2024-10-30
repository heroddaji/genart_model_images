import { z } from "zod";
import config from "../config";

const ComfyNodeSchema = z.object({
  inputs: z.any(),
  class_type: z.string(),
  _meta: z.any().optional(),
});

type ComfyNode = z.infer<typeof ComfyNodeSchema>;

interface Workflow {
  RequestSchema: z.ZodObject<any, any>;
  generateWorkflow: (input: any) => Record<string, ComfyNode>;
  description?: string;
  summary?: string;
}

const RequestSchema = z.object({
  image: z.string().describe("Path or filename of the input image to upscale"),
  upscale_model: z
    .enum(["RealESRGAN_x2.pth","RealESRGAN_x4.pth"])
    .default("RealESRGAN_x2.pth")
    .describe("The upscaling model to use")
});

type InputType = z.infer<typeof RequestSchema>;

function generateWorkflow(input: InputType): Record<string, ComfyNode> {
  return {
    "2": {
      inputs: {
        model_name: input.upscale_model
      },
      class_type: "UpscaleModelLoader",
      _meta: {
        title: "Load Upscale Model"
      }
    },
    "3": {
      inputs: {
        image: input.image,
        upload: "image"
      },
      class_type: "LoadImage",
      _meta: {
        title: "Load Image"
      }
    },
    "4": {
      inputs: {
        upscale_model: ["2", 0],
        image: ["3", 0]
      },
      class_type: "ImageUpscaleWithModel",
      _meta: {
        title: "Upscale Image (using Model)"
      }
    },
    "6": {
      inputs: {
        filename_prefix: "genart",
        file_type: "WEBP (lossy)",
        images: ["4", 0]
      },
      class_type: "SaveImageExtended",
      _meta: {
        title: "Save Image (Extended)"
      }
    }
  };
}

const workflow: Workflow = {
  RequestSchema,
  generateWorkflow,
};

export default workflow;
