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

let checkpoint: any = config.models.checkpoints.enum.optional();
if (config.warmupCkpt) {
  checkpoint = checkpoint.default(config.warmupCkpt);
}

const RequestSchema = z.object({
  prompt: z
    .string()
    .describe("The positive prompt for image generation"),
  batch_size: z
    .number()
    .int()
    .min(1)
    .max(8)
    .optional()
    .default(1)
    .describe("Batch size"),
  width: z
    .number()
    .int()
    .min(256)
    .max(2048)
    .optional()
    .default(1024)
    .describe("Width of the generated image"),
  height: z
    .number()
    .int()
    .min(256)
    .max(2048)
    .optional()
    .default(1024)
    .describe("Height of the generated image"),
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
    .default(5)
    .describe("Number of sampling steps"),
  cfg_scale: z
    .number()
    .min(0)
    .max(20)
    .optional()
    .default(1)
    .describe("Classifier-free guidance scale"),
  guidance: z
    .number()
    .min(0)
    .max(20)
    .optional()
    .default(4)
    .describe("Flux guidance scale"),
  sampler_name: config.samplers
    .optional()
    .default("euler")
    .describe("Name of the sampler to use"),
  scheduler: config.schedulers
    .optional()
    .default("beta")
    .describe("Type of scheduler to use"),
  denoise: z
    .number()
    .min(0)
    .max(1)
    .optional()
    .default(1)
    .describe("Denoising strength"),
});

type InputType = z.infer<typeof RequestSchema>;

function generateWorkflow(input: InputType): Record<string, ComfyNode> {
  return {
    "6": {
      inputs: {
        text: input.prompt,
        clip: ["36", 0]
      },
      class_type: "CLIPTextEncode",
      _meta: {
        title: "CLIP Text Encode (Prompt)"
      }
    },
    "8": {
      inputs: {
        samples: ["29", 0],
        vae: ["35", 0]
      },
      class_type: "VAEDecode",
      _meta: {
        title: "VAE Decode"
      }
    },
    "26": {
      inputs: {
        guidance: input.guidance,
        conditioning: ["6", 0]
      },
      class_type: "FluxGuidance",
      _meta: {
        title: "FluxGuidance"
      }
    },
    "29": {
      inputs: {
        seed: input.seed,
        steps: input.steps,
        cfg: input.cfg_scale,
        sampler_name: input.sampler_name,
        scheduler: input.scheduler,
        denoise: input.denoise,
        model: ["33", 0],
        positive: ["26", 0],
        negative: ["31", 0],
        latent_image: ["32", 0]
      },
      class_type: "KSampler",
      _meta: {
        title: "KSampler"
      }
    },
    "31": {
      inputs: {
        text: "",
        clip: ["36", 0]
      },
      class_type: "CLIPTextEncode",
      _meta: {
        title: "CLIP Text Encode (Prompt)"
      }
    },
    "32": {
      inputs: {
        width: input.width,
        height: input.height,
        batch_size: input.batch_size
      },
      class_type: "EmptyLatentImage",
      _meta: {
        title: "Empty Latent Image"
      }
    },
    "33": {
      inputs: {
        unet_name: "flux1-schnell-Q4_K_S.gguf"
      },
      class_type: "UnetLoaderGGUF",
      _meta: {
        title: "Unet Loader (GGUF)"
      }
    },
    "35": {
      inputs: {
        vae_name: "ae.safetensors"
      },
      class_type: "VAELoader",
      _meta: {
        title: "Load VAE"
      }
    },
    "36": {
      inputs: {
        clip_name1: "t5xxl_fp8_e4m3fn.safetensors",
        clip_name2: "clip_l.safetensors",
        type: "flux"
      },
      class_type: "DualCLIPLoaderGGUF",
      _meta: {
        title: "DualCLIPLoader (GGUF)"
      }
    },
    "40": {
      inputs: {
        filename_prefix: "genart",
        file_type: "WEBP (lossy)",
        images: ["8", 0]
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