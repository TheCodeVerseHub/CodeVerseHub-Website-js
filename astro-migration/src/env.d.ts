/// <reference path="../.astro/types.d.ts" />

interface ImportMetaEnv {
  readonly ADMIN_USER: string;
  readonly ADMIN_PASS: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}