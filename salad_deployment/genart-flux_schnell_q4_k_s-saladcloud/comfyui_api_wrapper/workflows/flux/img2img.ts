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
  prompt: z
    .string()    
    .default("Bubble Bobble style. 8-bit, cute, pixelated, fantasy, vibrant, reminiscent of Bubble Bobble game")
    .describe("The positive prompt for image generation"),
  image: z
    .string()
    .describe("Base64 encoded image or path to image file"),
  seed: z
    .number()
    .int()
    .optional()
    .default(() => Math.floor(Math.random() * 1000000000000000))
    .describe("Seed for random number generation"),
  steps: z
    .number()
    .int()
    .min(1)
    .max(100)
    .optional()
    .default(20)
    .describe("Number of sampling steps"),
  denoise: z
    .number()
    .min(0)
    .max(1)
    .optional()
    .default(0.75)
    .describe("Denoising strength"),
});

type InputType = z.infer<typeof RequestSchema>;

function generateWorkflow(input: InputType): Record<string, ComfyNode> {
  return {
    "6": {
      inputs: {
        text: input.prompt,
        clip: ["11", 0],
      },
      class_type: "CLIPTextEncode",
      _meta: {
        title: "CLIP Text Encode (Prompt)",
      },
    },
    "8": {
      inputs: {
        samples: ["13", 0],
        vae: ["10", 0],
      },
      class_type: "VAEDecode",
      _meta: {
        title: "VAE Decode",
      },
    },
    "10": {
      inputs: {
        vae_name: "ae.safetensors",
      },
      class_type: "VAELoader",
      _meta: {
        title: "Load VAE",
      },
    },
    "11": {
      inputs: {
        clip_name1: "t5xxl_fp8_e4m3fn.safetensors",
        clip_name2: "clip_l.safetensors",
        type: "flux",
      },
      class_type: "DualCLIPLoader",
      _meta: {
        title: "DualCLIPLoader",
      },
    },
    "13": {
      inputs: {
        noise: ["25", 0],
        guider: ["22", 0],
        sampler: ["16", 0],
        sigmas: ["17", 0],
        latent_image: ["30", 0],
      },
      class_type: "SamplerCustomAdvanced",
      _meta: {
        title: "SamplerCustomAdvanced",
      },
    },
    "16": {
      inputs: {
        sampler_name: "ipndm",
      },
      class_type: "KSamplerSelect",
      _meta: {
        title: "KSamplerSelect",
      },
    },
    "17": {
      inputs: {
        scheduler: "beta",
        steps: input.steps,
        denoise: input.denoise,
        model: ["31", 0],
      },
      class_type: "BasicScheduler",
      _meta: {
        title: "BasicScheduler",
      },
    },
    "22": {
      inputs: {
        model: ["31", 0],
        conditioning: ["6", 0],
      },
      class_type: "BasicGuider",
      _meta: {
        title: "BasicGuider",
      },
    },
    "25": {
      inputs: {
        noise_seed: input.seed,
      },
      class_type: "RandomNoise",
      _meta: {
        title: "RandomNoise",
      },
    },
    "26": {
      inputs: {
        image: input.image,
        upload: "image",
      },
      class_type: "LoadImage",
      _meta: {
        title: "Load Image",
      },
    },
    "29": {
      inputs: {
        upscale_method: "lanczos",
        megapixels: 1,
        image: ["26", 0],
      },
      class_type: "ImageScaleToTotalPixels",
      _meta: {
        title: "ImageScaleToTotalPixels",
      },
    },
    "30": {
      inputs: {
        pixels: ["29", 0],
        vae: ["10", 0],
      },
      class_type: "VAEEncode",
      _meta: {
        title: "VAE Encode",
      },
    },
    "31": {
      inputs: {
        unet_name: "flux1-schnell-Q4_K_S.gguf",
        dequant_dtype: "default",
        patch_dtype: "default",
        patch_on_device: false,
      },
      class_type: "UnetLoaderGGUFAdvanced",
      _meta: {
        title: "Unet Loader (GGUF/Advanced)",
      },
    },
    "33": {
      inputs: {
        filename_prefix: "ComfyUI",
        file_type: "WEBP (lossy)",
        images: ["8", 0],
      },
      class_type: "SaveImageExtended",
      _meta: {
        title: "Save Image (Extended)",
      },
    },
  };
}

const workflow: Workflow = {
  RequestSchema,
  generateWorkflow,
};

export default workflow;