/** Ogre drawn for this app: pointed ears, heavy brow and two tusks. */

export default function OgreIcon({ size = 24, className }: { size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="2 2.2 20 19.6" className={className} fill="none" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
      <path d="M6 10c0-4 2.4-7 6-7s6 3 6 7v4c0 4-2.6 7-6 7s-6-3-6-7z" />
      <path d="M6 9.6 2.4 7.4c-.3 2.8.9 4.9 3.6 5.6M18 9.6l3.6-2.2c.3 2.8-.9 4.9-3.6 5.6" />
      <path d="m8.2 8.2 2.8 1.3M15.8 8.2 13 9.5" />
      <path d="M11 13.2c.6.5 1.4.5 2 0" />
      <path d="M8.6 16.8h6.8M9.5 16.8l.7-1.9.8 1.9M13 16.8l.8-1.9.7 1.9" />
      <circle cx="9.8" cy="11" r=".7" fill="currentColor" stroke="none" />
      <circle cx="14.2" cy="11" r=".7" fill="currentColor" stroke="none" />
    </svg>
  )
}
