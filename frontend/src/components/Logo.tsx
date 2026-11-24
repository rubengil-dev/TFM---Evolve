/** Logo of the app: a leaf inside a circle whose veins are an AI network; the tab icon is a simpler copy in public/. */

export default function Logo({ size = 40 }: { size?: number }) {
  return (
    <svg width={size} height={size} viewBox="0 0 64 64" fill="none" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <circle cx="32" cy="32" r="29.25" stroke="#1F6B4E" strokeWidth="3.5" />
      <g transform="rotate(32 32 32) translate(1.92 1.92) scale(.94)">
        <path
          d="M32 6C36 15 49.5 22 48.5 37C48 46.5 40 53 32 54C24 53 16 46.5 15.5 37C14.5 22 28 15 32 6ZM32 54V58"
          stroke="#34D399"
          strokeWidth="3.4"
        />
        <path d="M32 47V17.5M32 47L22.5 38M32 47L41.5 38M32 32L24.5 24.5M32 32L39.5 24.5" stroke="#A7F3D0" strokeWidth="1.5" />
        <g fill="#A7F3D0">
          <circle cx="32" cy="47" r="2.9" />
          <circle cx="32" cy="32" r="2.5" />
          <circle cx="32" cy="17.5" r="2.6" />
          <circle cx="22.5" cy="38" r="2.6" />
          <circle cx="41.5" cy="38" r="2.6" />
          <circle cx="24.5" cy="24.5" r="2.5" />
          <circle cx="39.5" cy="24.5" r="2.5" />
        </g>
      </g>
    </svg>
  )
}
