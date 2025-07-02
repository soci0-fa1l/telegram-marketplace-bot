/// <reference types="react-scripts" />

declare module 'react-dom' {
  export function render(
    element: React.ReactElement,
    container?: Element | DocumentFragment | null,
    callback?: () => void
  ): void;
}
